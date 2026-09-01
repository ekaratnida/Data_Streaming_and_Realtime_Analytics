# Exercise scenario

## ให้ นศ สร้างระบบ data streaming & real-time analytics ดังนี้

เป็นระบบเกี่ยวกับการให้ rating movie โดยมีข้อกำหนดดังนี้
### 1. Kafka มีทั้งหมด 3 brokers, 1 zookeeper, schema register, and kafka ui
- Show the captured screen of the Docker container

### 2. มี 1 topic ชื่อ movie โดยแบ่งเป็น 4 partitions และ 3 replication factors
- Show the captured screen of the Kafka dashboard

### 3. สร้าง Schema v.1 โดยใช้ Kafka dashboard และให้ตั้งชื่อ subject ว่าอะไร เพื่อที่จะให้สอดคล้องกับ topic movie ในข้อ 2.
```Json
{
  "namespace": "example.avro",
  "type": "record",
  "name": "Movie",
  "fields": [
    {"name": "movieId", "type": "int"},
    {"name": "title", "type": "string"},
    {"name": "genres", "type": "string"},
    {"name": "rating", "type": "double"}
  ]
}
```
- Show the captured screen of the Kafka dashboard

### 4. Modify และ run 'producer_avro2.py' เพื่อให้ส่งข้อมูลไป Topic 'movie' ด้วย Schema v.1
- Show the captured screen of the Kafka dashboard

### 5. Modify และ run 'consumer_avro2.py' เพื่อให้รับข้อมูลจาก Topic 'movie' ด้วย Schema v.1
- Show the captured screen of your terminal

### 6. ให้ดัดแปลง Schema v.1 ไปเป็น v.2 โดยให้ลบ field 'rating' ออก และใช้ Backward compat mode
- Show the captured screen of the Kafka dashboard

### 7. Modify และเปลี่ยนชื่อจาก 'consumer_avro2.py' เป็น 'consumer_avro3.py' และ run เพื่อให้รับข้อมูลจาก Topic 'movie' ด้วย Schema v.2
- Show the captured screen of your terminal

~~### 8. Run 'consumer_avro2.py' เพื่อให้รับข้อมูลจาก Topic 'movie' ด้วย Schema v.1 และสังเกตผลลัพธ์~~ (This question duplicates with q5)
~~- Show the captured screen of your terminal~~

### 9. สร้าง scenario เพื่อทดสอบ Forward Compat Mode
- Show your results

