START /b /wait cmd /C "C:\kafka_2.13-2.7.0\bin\windows\kafka-topics.bat --bootstrap-server ec2-13-229-46-113.ap-southeast-1.compute.amazonaws.com:9092 --delete --topic streams-pageview-input"

START /b /wait cmd /C "C:\kafka_2.13-2.7.0\bin\windows\kafka-topics.bat --bootstrap-server ec2-13-229-46-113.ap-southeast-1.compute.amazonaws.com:9092 --delete --topic streams-userprofile-input"

START /b /wait cmd /C "C:\kafka_2.13-2.7.0\bin\windows\kafka-topics.bat --bootstrap-server ec2-13-229-46-113.ap-southeast-1.compute.amazonaws.com:9092 --delete --topic streams-pageviewstats-untyped-output"

pause