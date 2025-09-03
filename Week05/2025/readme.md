### Lecture note
https://docs.google.com/document/d/1R7SqaHRGVkOy_ctLv-IdqYqNDChFF5zMPOZayR7KCaM/edit?tab=t.0

### Todo
1. Use https://downgit.github.io/ to download folder 2025 from this github.
2. Run ```docker compose up -d``` inside source and sink_and_kafka
3.Change ip address inside source.json to your real ip address at that time.
4. Open 'control-center service' by clicking at port 9021
5. Click 'connector' -> 'add connector' -> upload source.json file -> launch.
6. Goto 'mysql' of source -> exec and run the following commands.
   ```
   mysql -uconfluent -pconfluent
   show databases;
   use connect_test;
   show tables;
   INSERT INTO movie (title, sale_ts, ticket_total_value) VALUES ('Aliens', '2019-07-18T10:00:00Z', 10);
   ```
7. At control-center, click menu topic -> you will see 'movie' topic -> streaming messaging updated every 5 seconds (because of 'bulk' mode)
8. Upload sink.json file to the same place at 5.
9. Goto 'mysql' of sink and run the same commands as 6. but use the select instead of insert and change the table from 'movie' to 'movie_tb'.

### 2. Example of timestamp
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
