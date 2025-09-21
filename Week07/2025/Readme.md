# How to Grafana
## Todo
1. python kafka_api3.py
2. python -m uvicorn kafka_api3:app --host 0.0.0.0 --port 8000
3. Click to view your data: http://localhost:8000/messages
4. set url in grafana json api: http://host.docker.internal:8000/messages
5. query: $.data[*]

# How to Flink
```sql
CREATE TABLE ratings (
    rating_id INT,
    title STRING,
    release_year INT,
    rating DOUBLE,
    ts TIMESTAMP(3),
    -- declare ts as event time attribute and use strictly ascending timestamp watermark strategy
    WATERMARK FOR ts AS ts
) WITH (
    'connector' = 'kafka',
    'topic' = 'ratings',
    'properties.bootstrap.servers' = 'broker:29092',
    'scan.startup.mode' = 'earliest-offset',
    'key.format' = 'raw',
    'key.fields' = 'rating_id',
    'value.format' = 'avro-confluent',
    'value.avro-confluent.url' = 'http://schema-registry:8081',
    'value.fields-include' = 'EXCEPT_KEY'
);
```
