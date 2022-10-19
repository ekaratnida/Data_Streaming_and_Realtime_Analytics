START /b /wait cmd /C "C:\kafka_2.13-2.7.0\bin\windows\kafka-topics.bat --create --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --replication-factor 3 --partitions 2 --topic streams-pageview-input"

START /b /wait cmd /C "C:\kafka_2.13-2.7.0\bin\windows\kafka-topics.bat --create --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --replication-factor 3 --partitions 2 --topic streams-userprofile-input"

START /b /wait cmd /C "C:\kafka_2.13-2.7.0\bin\windows\kafka-topics.bat --create --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --replication-factor 3 --partitions 2 --topic streams-pageviewstats-untyped-output"

pause
