CREATE DATABASE IF NOT EXISTS connect_test;
USE connect_test;

DROP TABLE IF EXISTS movie_tb;

CREATE TABLE connect_test.movie_tb ( 
  id INT NOT NULL AUTO_INCREMENT, 
  title VARCHAR(100) NOT NULL, 
  sale_ts DATETIME NOT NULL, 
  ticket_total_value INT NOT NULL, 
  PRIMARY KEY (id)
);
