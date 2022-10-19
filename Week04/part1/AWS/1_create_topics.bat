START /b /wait cmd /C "C:\kafka_2.13-2.7.0\bin\windows\kafka-topics.bat --create --bootstrap-server ec2-13-229-46-113.ap-southeast-1.compute.amazonaws.com:9092 --replication-factor 1 --partitions 1 --topic streams-pageview-input"

START /b /wait cmd /C "C:\kafka_2.13-2.7.0\bin\windows\kafka-topics.bat --create --bootstrap-server ec2-13-229-46-113.ap-southeast-1.compute.amazonaws.com:9092 --replication-factor 1 --partitions 1 --topic streams-userprofile-input"

START /b /wait cmd /C "C:\kafka_2.13-2.7.0\bin\windows\kafka-topics.bat --create --bootstrap-server ec2-13-229-46-113.ap-southeast-1.compute.amazonaws.com:9092 --replication-factor 1 --partitions 1 --topic streams-pageviewstats-untyped-output"

pause
