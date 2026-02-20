# Todo
1. Use [https://downgit.github.io/](https://downgit.github.io/) to download the folder **2025** from this GitHub repository.  

2. Run the following command inside both the **source**, **sink**, and **kafka** directories:  
   ```bash
   docker compose up -d
   ```
3. Change the IP address inside source.json and sink.json to your actual IP address at runtime.
4. Open the Kafka UI.
5. Upload source.json file → Launch.
6. Go to the MySQL container of the source, then run:
```sql
mysql -uconfluent -pconfluent
show databases;
use connect_test;
show tables;
INSERT INTO movie (title, sale_ts, ticket_total_value) 
VALUES ('Aliens', '2019-07-18T10:00:00Z', 10);
```
7. In Kafka UI, You should see the movie topic updating every 5 seconds (because of “bulk” mode).
8. Upload the sink.json file to the same location as in Step 5.
9. Go to the MySQL container of the sink and run the same commands as in Step 6, but use SELECT instead of INSERT, and change the table name from movie to movie_tb.

# Exercise
1. Use 'incrementing' mode instead of 'bulk' mode. (should one column (number data type)
2. Use 'timestamp' mode instead of bulk mode. (should one column (timestamp type)
3. Use 'timestamp+incrementing' mode instead of bulk mode. (should two columns (number and timestamp)

## Miscellaneous
- Example of timestamp
```
{
    "type" : "record",
    "name" : "schema",
    "fields" : [{
        "name" : "entryDate",
        "type" : ["null", {
            "type" : `**"string"**`,
            "logicalType" : "timestamp-micros"
        }],
        "default" : null
    }]
}
```
<img width="964" height="624" alt="image" src="https://github.com/user-attachments/assets/23dd6cec-81fa-49b9-ab0a-043437005145" />


CREATE TABLE `connect_test`.`movie2` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL,
  `sale_ts` DATETIME NOT NULL,
  `ticket_total_value` INT NOT NULL,
  PRIMARY KEY (`id`));


CREATE TABLE `connect_test`.`movie2_tb` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL,
  `sale_ts` DATETIME NOT NULL,
  `ticket_total_value` INT NOT NULL,
  PRIMARY KEY (`id`));

Prompt:

create an automated script that first runs docker-compose in kafka, and then the docer-compose inside the
  sink folder, and then the docker-compose inside the source folder. Later, the automated script includes the
  curl for sink2.json, then the curl for  source-timestamp-incrementing.json finally.
  
