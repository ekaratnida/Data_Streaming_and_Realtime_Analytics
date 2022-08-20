# Part 1 - Setup and Prerequisites

## Kafka overview

[Apache Kafka](https://kafka.apache.org) is a distributed streaming platform. It provides publish-subscribe APIs and can store and process streams of records at large scale.

Kafka is made up of the following components:
- <b> Cluster </b> : A Kafka cluster consists of one or more servers (Kafka brokers) running Kafka
- <b> Broker (or server) </b> : One of more brokers form a Kafka cluster
- <b> Producer </b> : Client to send records into Kafka
- <b> Consumer </b> : Client to read records from Kafka

![Kafka architecture](https://user-images.githubusercontent.com/69342162/128960348-ca77f81b-a858-4107-b5c8-a76239932b92.png)
*Kafka architecture: image refered from https://data-flair.training/blogs/kafka-architecture/*

You can learn more about Kafka in this introductory article,

"[What is Apache Kafka](https://developer.ibm.com/articles/an-introduction-to-apache-kafka/)" 

or in this conference presentation, 

"[Introducing Apache Kafka](https://developer.ibm.com/videos/an-introduction-to-apache-kafka/)."

## Prerequisites for this workshop

In order to complete this workshop, you need to have the following dependencies installed:

- [Java SDK](https://jdk.java.net/java-se-ri/10), Version 10
- Accept License Agreement --> Unzip --> //Set Environment path
- java -version

## Downloading Apache Kafka

In this workshop, we will use the Kafka command line tools.

[Download](https://drive.google.com/drive/folders/1FTdo0sqTpUwRl4EBtFBbXt6fRjtjAbi6?usp=sharing) binary package from the Apache Kafka website, unzip it, and move the folder to drive c.

!!! Put kafka folder in drive D may cause the problem (long sth)

## Setup Kafka cluster
# Setting up Apache Kafka on a local machine

Follow these steps if you want to set up a 3-broker Kafka cluster on a single machine. This environment is not suitable for production, but it provides all the features necessary to complete this workshop.

## 1) Starting ZooKeeper

The first step is to get ZooKeeper running. This is necessary in order to start Kafka:

We can start ZooKeeper with the default configuration file, by running the following command when you are in c:\kafka-2.13-3.2.1\ path,

```sh
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

May be an existing issue: https://stackoverflow.com/a/65466930

We have now started a ZooKeeper ensemble consisting of a single server. Again, this is not suitable for production but it is enough to start a Kafka cluster.

## Configuring a local Kafka cluster

Kafka provides a default Kafka configuration file, `config\server.properties`. We will reuse this file and make a few changes.

1. Make the three copies of `config\server.properties` and named them as:
    - `config\server0.properties`
    - `config\server1.properties`
    - `config\server2.properties`

2. In each of three files:
    - Replace line 21 with `broker.id=<BROKER_ID>`
    - Replace line 31 with `listeners=PLAINTEXT://:9<BROKER_ID>92`
    - Replace line 60 with `log.dirs=/tmp/kafka<BROKER_ID>-logs`
    
    `where <BROKER_ID>` is the number of the file name, 
     
    ```html
        For example, `config/server2.properties` includes
        - `broker.id=2`
        - `listeners=PLAINTEXT://:9292`
        - `log.dirs=/tmp/kafka2-logs`
    ```
    
    - Replace lines from 74 to 76 with:

    ```properties
    offsets.topic.replication.factor=3
    transaction.state.log.replication.factor=3
    transaction.state.log.min.isr=3
    ```

## 2) Starting the Kafka cluster

Now that we have all the required configurations, let's start our brokers (C:\kafka_2.13-3.2.1):

```sh
bin\windows\kafka-server-start.bat config\server0.properties
```

Then, open a new terminal window and run:

```sh
bin\windows\kafka-server-start.bat config\server1.properties
```

Then, open a new terminal window and run:
```sh
bin\windows\kafka-server-start.bat config\server2.properties
```

Congratulations, you've now started your Kafka cluster!

```html
Note that if a server is off,
(1) close all terminals,
(2) delete all existing folders and files in "C:\tmp" and "C:\kafka_2.13-3.2.1\logs", and 
(3) run again.
```

After this, you can use script from Week3 part1 to automately run the Kafka Cluster

## Menu
Continue to [part 2](../part2/README.md)

Return to [Week02](../README.md)




