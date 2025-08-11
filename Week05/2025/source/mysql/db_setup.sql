CREATE DATABASE IF NOT EXISTS connect_test;
USE connect_test;

DROP TABLE IF EXISTS movie;

CREATE TABLE IF NOT EXISTS movie (
  title varchar(100) not null,
  sale_ts varchar(100) not null,
  ticket_total_value int not null
);