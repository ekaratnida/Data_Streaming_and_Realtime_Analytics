# How to Grafana
## Todo

python -m uvicorn kafka_api:app --host 0.0.0.0 --port 8000

http://host.docker.internal:8000/messages

$.data[*]

## View data

http://localhost:8000/messages

# How to Flink
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
