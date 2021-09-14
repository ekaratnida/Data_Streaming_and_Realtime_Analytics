# Week6 (Outline)** ::hurtrealbad::hurtrealbad:

## 6.1 What you've learned so far.
<img src=./img1.png width="800" height="600">

## 6.2 Lecture
### Mobile sensors and user behaviors
- Mobile-sensor.pdf

## 6.3 Lab
### Spark streaming
- Run "Week6_spark.ipynb" in colab
- https://spark.apache.org/docs/latest/streaming-programming-guide.html

*********************************************************************


## (Optional, not need to setup this in class) 6.3.1 Setup and run Spark on local machine
  1. Install java (version 8)
  2. Install python
  3. Download spark https://downloads.apache.org/spark/spark-2.4.7/spark-2.4.7-bin-hadoop2.6.tgz
  4. Setup spark home SPARK_HOME=C:\spark-2.4.7-bin-hadoop2.6\
  5. Test run "pyspark"

  For window only

  6. Create a hadoop\bin folder inside the SPARK_HOME folder

  7. Download http://github.com/steveloughran/winutils/raw/master/hadoop-2.6.0/bin/winutils.exe to hadoop\bin

  8. Setup hadoop home HADOOP_HOME=%SPARK_HOME%\hadoop

  **To run program (Wordcount)**

  0. pip install findspark
  1. Start a kafker cluster (zoo + brokers)
  2. Create a topic
  3. Download the "spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar" file from https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-kafka-0-8-assembly_2.11/2.4.7 or from this github to drive C:\
  4. :+1: Run the following command 
  ```
  spark-submit --jars C:\spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar kafka_spark_demo.py
  ```
  in C:\Users\STD User\kafka-quickstart-workshop-main\Week6>

  5. Run a producer to generate a list of words

  ### *Note*
  Must use python 3.7 and Java 8

  <!--
  ### 6.3.2 Setup and run Spark on colab
  https://nb.recohut.com/spark/pyspark/kafka/movie/2021/06/25/kafka-spark-streaming-colab.html
  -->
  
  Dataset --> https://grouplens.org/datasets/movielens/
