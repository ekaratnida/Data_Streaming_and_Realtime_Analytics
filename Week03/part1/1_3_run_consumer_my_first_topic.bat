START /b /wait cmd /C "C:\kafka_2.13-2.7.0\bin\windows\kafka-console-consumer.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --topic mqtt-topic --from-beginning"
