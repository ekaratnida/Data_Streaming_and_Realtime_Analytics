# Stream data cleansing

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