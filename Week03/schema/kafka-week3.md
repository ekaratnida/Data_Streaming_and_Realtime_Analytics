# Exercise scenario

## ให้ นศ สร้างระบบ data streaming & real-time analytics ดังนี้

เป็นระบบเกี่ยวกับการให้ rating movie โดยมีข้อกำหนดดังนี้
### 1. Kafka มีทั้งหมด 3 brokers, 1 zookeeper, schema register, and kafka ui
- show docker container screen

### 2. มี 1 topic ชื่อ movie โดยแบ่งเป็น 4 partitions และ 3 replication factors
- show kafka dashboard screen (schema register)

### 3. Producer1 เป็น python code โดยมีข้อมูลดังนี้
- show producer1 python code screen

### 4. consumer1 เป็น python code โดยรับข้อมูลทั้งหมดมา print แสดงผล
- show consumer1 python code screen

### 5. การส่งข้อมูลระหว่าง producer1 และ consumer1 ต้องมีการใช้ schema version 1 ด้วย
- show kafka dashboard screen

### 6. ต่อมาฝั่ง business ต้องการตัด field x ทิ้ง (version 2) และมีเงื่อนไขว่าจะมี consumer2 เท่านั้นที่รับข้อมูล version 2 ได้ส่วน consumer1 จะรับข้อมูลได้แค่ version 1 เท่านั้น
- show kafka dashboard screen (schema register)
