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

use `elastic.yml`.

1. Start docker
```bash
docker compose -f elastic.yml up -d
```

2. Create the index with an explicit mapping, before starting any job

```bash
curl -X PUT "http://localhost:9200/faker_orders" -H "Content-Type: application/json" --data-binary @create.json
```

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

7.1) Stack Management -> Index Patterns (Kibana) -> create index pattern -> `faker_orders*` -> edit -> Time field -> `order_time` -> click 'create_index_pattern'.

7.2) Analytic -> Discover 

8. Verify
```bash
curl "http://localhost:9200/faker_orders/_count"
```

The count should climb while the job runs.
