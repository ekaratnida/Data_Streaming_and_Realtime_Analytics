# Lecture note
https://docs.google.com/document/d/1R7SqaHRGVkOy_ctLv-IdqYqNDChFF5zMPOZayR7KCaM/edit?tab=t.0

# Todo
1. Use [https://downgit.github.io/](https://downgit.github.io/) to download the folder **2025** from this GitHub repository.  
2. Run the following command inside both the **source** and **sink_and_kafka** directories:  
   ```bash
   docker compose up -d
   ```
3. Change the IP address inside source.json to your actual IP address at runtime.
4. Open the Control Center service by accessing port 9021.
5. Click Connector → Add Connector → Upload source.json file → Launch.
6. Go to the MySQL container of the source, then run:
```sql
mysql -uconfluent -pconfluent
show databases;
use connect_test;
show tables;
INSERT INTO movie (title, sale_ts, ticket_total_value) 
VALUES ('Aliens', '2019-07-18T10:00:00Z', 10);
```
7. In Control Center, go to the Topics menu. You should see the movie topic updating every 5 seconds (because of “bulk” mode).
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
- If you want to try 'metabase' dashboard
```
 metabase:
    image: metabase/metabase:latest
    container_name: metabase
    ports:
      - "3000:3000"
    environment:
      # Metabase application DB (internal) - optional: default H2 is fine for testing.
      # If you want PostgreSQL for Metabase internal DB, set METABASE_DB_* here.
      MB_ENCRYPTION_SECRET_KEY: "0123456789abcdef"
    depends_on:
      - quickstart-mysql   # ensures MySQL is started first
    restart: unless-stopped
```
