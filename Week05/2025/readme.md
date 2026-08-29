# Todo
1. Use [https://downgit.github.io/](https://downgit.github.io/) to download the folder **2025** from this GitHub repository.  

2. Run the following command inside (1) the **source**, (2) **sink**, and (3) **kafka** directories (Run 3 times):  
   ```bash
   docker compose up -d
   ```

3. Change the IP address inside the source_bulk.json and sink.json to your current IP address.

4. Open the Kafka UI -> Kafka connect -> Create connector.

5. Use the information from source_bulk.json to create a new connector and then submit as shown in the image below.
   <img width="1029" height="722" alt="image" src="https://github.com/user-attachments/assets/aa90757d-d091-4f7c-bdd9-beac2a81d64f" />
   5.1 if it works, you can see the running created connector.
   <img width="1895" height="371" alt="image" src="https://github.com/user-attachments/assets/fa899048-ffed-4435-9759-7f2a55170b94" />

6. Go to Source container, click mysql-source, click Exec, then paste the mysql command below inside the Exec:
```sql
mysql -uconfluent -pconfluent
show databases;
use connect_test;
show tables;
INSERT INTO movie (title, sale_ts, ticket_total_value) 
VALUES ('Aliens', '2019-07-18 10:00:00', 10);
```

7. In Kafka UI, You should see the movie topic updating every 5 seconds (because of the “bulk” mode).

8. Insert a new data and observe the result
```sql
INSERT INTO movie (title, sale_ts, ticket_total_value) 
VALUES ('Cat', '2019-07-18 11:00:00', 20);
```

9. Use the information from sink.json to create a new connector and then submit as shown in the image below.

10. Go to Sink container, click mysql-sink, click Exec, then paste the mysql command below inside the Exec:
```sql
mysql -uc -pc
show databases;
use connect_test;
show tables;
SELECT * from movie_tb;
```
10. Observe the results in movie_tb.

# Exercise
1. Use 'incrementing' mode instead of 'bulk' mode. (select one column (as number data type)
2. Use 'timestamp' mode instead of bulk mode. (select one column (as timestamp type)
3. Use 'timestamp+incrementing' mode instead of bulk mode. (select two columns (as number and timestamp type)


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
  
