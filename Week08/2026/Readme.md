# Stream data cleansing

Uses `docker-compose-flinksql-grafana.yml`, which does not include
Elasticsearch or Kibana. For the Elasticsearch section further down, use
`elastic.yml` instead.

1. Start docker
```bash
docker compose -f docker-compose-flinksql-grafana.yml up -d
```

2. Start flinksql client
```bash
docker exec -it flink-sql-client sql-client.sh
```

3. Create a source table
```sql
CREATE TABLE raw_user_clicks (
  user_id INT,
  email STRING,
  search_query STRING,
  click_count INT,
  raw_timestamp TIMESTAMP(3),
  WATERMARK FOR raw_timestamp AS raw_timestamp - INTERVAL '5' SECOND
) WITH (
  'connector' = 'faker',
  'fields.user_id.expression' = '#{number.numberBetween ''100'',''999''}',
  'fields.email.expression' = '#{Internet.emailAddress}',
  'fields.search_query.expression' = '  #{Lorem.words ''2''}  ',
  'fields.click_count.expression' = '#{number.numberBetween ''-5'',''20''}',
  'fields.raw_timestamp.expression' = '#{date.past ''10'',''SECONDS''}',
  'rows-per-second' = '5'
);
```
4. Create a sink table
```sql
CREATE TABLE clean_user_clicks (
  user_id INT,
  email STRING,
  search_query STRING,
  click_count INT,
  event_time TIMESTAMP(3),
  PRIMARY KEY (user_id) NOT ENFORCED
) WITH (
  'connector' = 'upsert-kafka',
  'topic' = 'clean_user_clicks',
  'properties.bootstrap.servers' = 'broker:9092',
  'key.format' = 'json',
  'value.format' = 'json'
);
```
5. sql
```sql
INSERT INTO clean_user_clicks (user_id, email, search_query, click_count, event_time)
SELECT 
  user_id,
  LOWER(TRIM(email)) AS email,
  TRIM(search_query) AS search_query,
  CASE WHEN click_count < 0 THEN 0 ELSE click_count END AS click_count,
  raw_timestamp AS event_time
FROM raw_user_clicks
WHERE email IS NOT NULL 
  AND TRIM(email) <> ''
  AND POSITION('@' IN email) > 0;
  ```

# Kibana and Elasticsearch

This section uses a different compose file. `docker-compose-flinksql-grafana.yml`
does not include Elasticsearch, Kibana, or the Elasticsearch connector jar, so
use `elastic.yml` instead.

1. Start docker
```bash
docker compose -f elastic.yml up -d
```

2. Create the index with an explicit mapping, before starting any job

This step is mandatory. The Elasticsearch connector serialises Flink's
`TIMESTAMP(3)` as a plain string, so if the index does not already exist,
Elasticsearch's dynamic mapping infers `text` for `order_time` on the very first
document. Field types are immutable once written, so it can never be corrected
with `PUT /faker_orders/_mapping` afterwards, and Kibana will not be able to
offer it as a time field.

```bash
curl -X PUT "http://localhost:9200/faker_orders" -H "Content-Type: application/json" --data-binary @create.json
```

`create.json` is in this directory. Note the `date` format must match the
connector's output exactly, hence the `.SSS`.

Do not declare `order_time` as `TIMESTAMP(3)` in the sink table. The connector
serialises a timestamp with trailing zeros trimmed from the fractional seconds,
so it emits `2026-09-26 16:06:30.49` rather than `2026-09-26 16:06:30.490`. That
does not match the `.SSS` format above, so roughly one document in ten is
rejected and the job dies with:

```
failed to parse date field [2026-09-26 16:06:30.49] with format [yyyy-MM-dd HH:mm:ss.SSS]
```

Declaring the column `STRING` and wrapping it in `DATE_FORMAT` in the `SELECT`
pins the width to exactly three digits instead.

3. Start flinksql client
```bash
docker exec -it flink-sql-client sql-client.sh
```

4. Create a source table
```sql
CREATE TABLE fake_orders (
  order_id STRING,
  user_name STRING,
  category STRING,
  price DOUBLE,
  quantity INT,
  order_time TIMESTAMP(3),
  WATERMARK FOR order_time AS order_time - INTERVAL '5' SECOND
) WITH (
  'connector' = 'faker',
  'fields.order_id.expression' = '#{Internet.uuid}',
  'fields.user_name.expression' = '#{Name.fullName}',
  'fields.category.expression' = '#{regexify ''(Electronics|Clothing|Home|Books|Beauty)''}',
  'fields.price.expression' = '#{number.randomDouble ''2'',''10'',''500''}',
  'fields.quantity.expression' = '#{number.numberBetween ''1'',''5''}',
  'fields.order_time.expression' = '#{date.past ''10'',''SECONDS''}',
  'rows-per-second' = '10'
);
```
5. Create a sink table

```sql
CREATE TABLE elastic_orders (
  order_id STRING,
  user_name STRING,
  category STRING,
  price DOUBLE,
  quantity INT,
  total_amount DOUBLE,
  order_time STRING,
  PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
  'connector' = 'elasticsearch-7',
  'hosts' = 'http://elasticsearch:9200',
  'index' = 'faker_orders',
  'format' = 'json'
);
```
6. Insert
```sql
INSERT INTO elastic_orders
SELECT 
  order_id,
  user_name,
  category,
  price,
  quantity,
  ROUND(price * quantity, 2) AS total_amount,
  DATE_FORMAT(order_time, 'yyyy-MM-dd HH:mm:ss.SSS') AS order_time
FROM fake_orders;
```

7. Point the Kibana data view at the timestamp field

Until this is set, Discover shows either "Select a timestamp field for use with
the global time filter" or "There are no available fields that contain data".

Stack Management -> Data Views -> `faker_orders*` -> edit -> Time field ->
`order_time`.

8. Verify
```bash
curl "http://localhost:9200/faker_orders/_count"
```

The count should climb while the job runs. If it stops at a small fixed number
and the job shows as failed, check `docker logs flink-jobmanager`.

# Troubleshooting

**The job fails with a `NullPointerException` in `DocWriteResponse`.**
The `elasticsearch-7` connector embeds a 7.17 client and cannot read bulk
responses from an 8.x server. `elastic.yml` pins Elasticsearch and Kibana to
7.17.9 for this reason. There is no `flink-sql-connector-elasticsearch8`; the
8.x connector is DataStream-only, with no SQL table factory, so it cannot be
used with `'connector' = ...` in SQL DDL.

**`mapper [order_time] cannot be changed from type [text] to [date]`.**
The index was created by dynamic mapping before step 2 was done. Elasticsearch
cannot change the type of an existing field, so the index has to be dropped and
recreated. Any data in it is lost.

**`failed to parse date field [...] with format [yyyy-MM-dd HH:mm:ss.SSS]`.**
`order_time` is declared `TIMESTAMP(3)` in the sink table, so the connector
trims trailing zeros from the fractional seconds and emits a variable-width
value that the mapping rejects. Declare it `STRING` and use
`DATE_FORMAT(order_time, 'yyyy-MM-dd HH:mm:ss.SSS')` in the `SELECT`.

**`resource_already_exists_exception` on step 2.**
The index already exists. Delete it first, which discards its documents:
```bash
curl -X DELETE "http://localhost:9200/faker_orders"
```