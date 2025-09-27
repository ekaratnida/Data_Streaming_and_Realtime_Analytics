# ================== แก้ไข Import ==================
# เปลี่ยนจาก Producer ธรรมดา + bson -> ใช้ AvroProducer
from confluent_kafka.avro import AvroProducer, loads
import random
from datetime import datetime
import time
 
# ================== กำหนด Avro Schema ==================
value_schema_str = """
{
  "namespace": "example.avro",
  "type": "record",
  "name": "Movie",
  "fields": [
    {"name": "title", "type": "string"},
    {"name": "sale_ts", "type": "string"},
    {"name": "ticket_total_value", "type": "int"}
  ]
}
"""
value_schema = loads(value_schema_str)
 
# ================== สร้าง AvroProducer ==================
avro_producer = AvroProducer(
    {
        'bootstrap.servers': 'localhost:8097',  # <-- ตรวจสอบพอร์ต Kafka ให้ถูกต้อง
        'schema.registry.url': 'http://localhost:8081'
    },
    default_value_schema=value_schema
)
 
titles = ["Name1", "Name2", "Name3"]
prices = [12, 24, 36]
 
# ================== ฟังก์ชัน callback ==================
def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % msg.value())  # <-- ไม่ต้อง decode เพราะ AvroProducer คืน dict
 
# ================== ส่งข้อมูล ==================
for i in range(10):
    current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    data = {
        'title': random.choice(titles),
        'sale_ts': current_time,
        'ticket_total_value': random.choice(prices)
    }
 
    avro_producer.produce(
        topic='movie',
        value=data,
        callback=acked   # <-- callback ใช้งานเหมือนเดิม
    )
    avro_producer.flush()
    time.sleep(random.randint(1, 5))