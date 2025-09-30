# How to Grafana
## Todo
1. Run "Producer_json.py".
2. Run ksqldb command.
```sql
CREATE STREAM movie_ticket_sales (title VARCHAR, sale_ts VARCHAR, ticket_total_value INT)
    WITH (KAFKA_TOPIC='movie-ticket-sales',
          PARTITIONS=1,
          VALUE_FORMAT='JSON');
  
CREATE TABLE movie_count WITH (VALUE_FORMAT = 'JSON') AS
  SELECT title, COUNT(*) AS tickets_sold
  FROM movie_ticket_sales
  WINDOW TUMBLING (SIZE 60 SECONDS)
  GROUP BY title
  EMIT CHANGES;
  ```
3. python kafka_api.py
4. python -m uvicorn kafka_api:app --host 0.0.0.0 --port 8000
5. Click to view your data: http://localhost:8000/messages
6. set url in grafana json api: http://host.docker.internal:8000/messages
7. query: $.data[*]

# How to Flink
```sql
CREATE TABLE movie_ticket_sales (
    title STRING,
    sales_ts STRING,
    total_ticket_value INT
) WITH (
    'connector' = 'kafka',
    'topic' = 'movie-ticket-sales',
    'properties.bootstrap.servers' = 'broker:29092',
    'scan.startup.mode' = 'earliest-offset',
    'key.format' = 'raw',
    'key.fields' = 'title',
    'value.format' = 'avro-confluent',
    'value.avro-confluent.url' = 'http://schema-registry:8081',
    'value.fields-include' = 'EXCEPT_KEY'
);


CREATE TABLE movie_count (
	title STRING,
	total_sales BIGINT,
	PRIMARY KEY (title) NOT ENFORCED
) WITH (
	'connector' = 'upsert-kafka',
	'topic' = 'movie-count',
	'properties.bootstrap.servers' = 'broker:29092',
	'key.format' = 'json',
	'value.format' = 'json'
);

insert into movie_count
select
 title,
 count(total_ticket_value) as total_sales
from movie_ticket_sales
group by title;
```
