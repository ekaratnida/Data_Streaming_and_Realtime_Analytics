1. download and install java
- https://www.oracle.com/java/technologies/downloads/#jdk17-windows
 
2. set path
- 2.1 Search "Edit the system environment variables"
- 2.2 Click "environment variables"
- 2.3 System variable -> path -> edit
- 2.4 insert jdk bin

3. Download git from
- https://developer.confluent.io/learn-kafka/kafka-streams/get-started/
- If fail, you may need to change the gradle version from 7.0 to 7.3

4. Change file type from "streams.properties.orig" to "streams.properties"

5. insert line "bootstrap.servers=localhost:9092" to streams.properties file

6. run command "gradlew runStreams -Pargs=basic" again
