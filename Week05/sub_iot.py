import microgear.client as client
import logging
import time

appid = "ekaratnida"
gearkey = 'jtD9ag08syPtqiK' # key
gearsecret = 'vDEEIuw9Ssj4OvbrBHmM4hZfa' # secret

client.create(gearkey,gearsecret,appid,{'debugmode': True}) # สร้างข้อมูลสำหรับใช้เชื่อมต่อ

client.setalias("ekarat") # ตั้งชื่้อ

def callback_connect() :
    print ("Now I am connected with netpie")
    
def callback_message(topic, message) :
    print(topic, ": ", message)

def callback_error(msg) :
    print("error", msg)

client.on_connect = callback_connect # แสดงข้อความเมื่อเชื่อมต่อกับ netpie สำเร็จ
client.on_message= callback_message # ให้ทำการแสดงข้อความที่ส่งมาให้
client.on_error = callback_error # หากมีข้อผิดพลาดให้แสดง
client.subscribe("/mobile") # ชื่อช่องทางส่งข้อมูล ต้องมี / นำหน้า และต้องใช้ช่องทางเดียวกันจึงจะรับส่งข้อมูลระหว่างกันได้
client.connect(True) # เชื่อมต่อ ถ้าใช้ True เป็นการค้างการเชื่อมต่อclient.on_message= callback_message # ให้ทำการแสดงข้อความที่ส่งมาให้