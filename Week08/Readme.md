1. Create a source table
```sql
CREATE TABLE raw_user_clicks (
  user_id INT,
  email STRING,
  search_query STRING,
  click_count INT,
  raw_timestamp BIGINT,
  event_time AS TO_TIMESTAMP_LTZ(raw_timestamp, 3),
  WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
  'connector' = 'faker',
  'fields.user_id.expression' = '#{number.numberBetween ''100'',''999''}',
  'fields.email.expression' = '#{Internet.emailAddress}',
  'fields.search_query.expression' = '  #{Lorem.words ''2''}  ', -- whitespace padding
  'fields.click_count.expression' = '#{number.numberBetween ''-5'',''20''}', -- negative values
  'fields.raw_timestamp.expression' = '#{date.past ''10'',''SECONDS''}',
  'rows-per-second' = '5'
);
```
