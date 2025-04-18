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
- http://spark.apache.org/docs/latest/structured-streaming-programming-guide.html

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
  
  Dataset 
  https://grouplens.org/datasets/movielens/
  
  Research
  https://mhealth.jmir.org/2021/3/e26320?fbclid=IwAR3qIindVGTzg4htMaJrc1EUnt4Ko-wcIXWKWghU77UEMScTLu7Vvq_A_W8
  
  %SPARK_HOME%\python;%SPARK_HOME%\python\lib\py4j-0.10.7-src.zip:%PYTHONPATH%
  
  
  ![image](https://user-images.githubusercontent.com/69342162/174016669-68d79c61-9fd1-4c94-b77b-b24983e01344.png)
  
  https://datamize.wordpress.com/2015/02/08/visualizing-basic-rdd-operations-through-wordcount-in-pyspark/
  
  ![image](https://user-images.githubusercontent.com/69342162/196129676-a4be6705-bf33-450c-a0ce-5328f87eb56d.png)


