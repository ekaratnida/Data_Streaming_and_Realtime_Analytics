# Exercise scenario

## ให้ นศ สร้างระบบ data streaming & real-time analytics ดังนี้

เป็นระบบเกี่ยวกับการให้ rating movie โดยมีข้อกำหนดดังนี้
### 1. Kafka มีทั้งหมด 3 brokers, 1 zookeeper, schema register, and kafka ui
- show docker container screen

### 2. มี 1 topic ชื่อ movie โดยแบ่งเป็น 4 partitions และ 3 replication factors
- show kafka dashboard screen (schema register)

### 3. Test the system using 'producer_avro.py' and 'consumer_avro.py'
- show the captured screen results of producer and consumer
### 4. Modify the schema v1 to v2 by deleting rating field
### 5. Test the system running 'producer_avro2.py', 'consumer_avro.py' and 'consumer_avro2.py'
- show the captured screen results of producer and two consumers.
