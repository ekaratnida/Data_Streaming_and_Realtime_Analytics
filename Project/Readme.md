## โจทย์ Final project

ให้เรารันระบบ airflow สามวัน ดังนี้
วันที่ 21, 22, 23 ธค โดยในแต่ละวันจะกำหนดช่วงเวลาในการ predict BTC ตั้งแต่ 22:00 ~ 6:00 โมงเช้า โดย schedule ทุกๆ 5 นาที และคำนวณ mape ทุกๆ ชั่วโมง (หมายถึง len=12)
โดย นศ จะส่ง mape.txt 3 files (ของช่วงวันเวลาที่ทดสอบ 3 วัน)  + code 3 dags + requirement.txt และ files อื่นๆ ถ้ามีความแตกต่างจาก starter kit 
กำหนด
1. dataset ในการสร้าง train และ predict model จะมี column (X=closeTime) และ (Y=lastPrice)
2. นศ สามารถใช้ regression model ต่างๆ หรือ เทคนิคทางด้าน time series หรือ AI มาช่วยวิเคราะห์ได้ 

## Link to Youtube
https://www.youtube.com/playlist?list=PLCY_u0_oBT6mx6PGR0VHSgnpNoPcKtH4F

