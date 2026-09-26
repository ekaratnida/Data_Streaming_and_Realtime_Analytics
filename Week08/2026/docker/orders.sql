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
