# Part 4 - Processing data with Kafka Streams

In this part of the workshop, we will learn about Kafka Streams and how it can be used to process streams of data in real time. Make sure that you've completed Part 3, since this part follows on from [Part 3](../part3/README.md).

![image](pipeline.png)

## Kafka Streams

[Kafka Streams](https://kafka.apache.org/documentation/streams/) is a client library for building applications and microservices, where the input and output data are stored in Kafka. It combines the simplicity of writing and deploying standard Java and Scala applications on the client-side with the benefits of Kafka's server-side cluster technology.

## Kafka Streams APIs

Kafka Streams exposes 2 APIs:

- **DSL**: This Domain Specific Language API makes it easy to express processing operations in just a few lines of code. This API is designed to allow most common use cases, making it especially easy to get started.

- **Processor**: This Processor API is lower level than the DSL API. This API gives developers full control and allows defining custom processors and accessing data stores.

Kafka Streams performs 1 record-at-a-time processing operations which enables near real-time processing of data. It also offers exactly-once processing semantics to ensure processing results are correct even in case of failure from the Kafka cluster or Kafka Streams itself.

## Processing Operations

There are 2 types of processing operations:

- **Stateless**: These transformations don't require Kafka Streams to keep state in order to be performed. Stateless operations include: filtering, branching, switching between KStreams and KTable abstractions, and so on.

- **Stateful**: These operations require Kafka Streams to maintain state in order to be performed. These include: joining, aggregating, and windowing.

A Kafka Streams application is a combination of processing operations linked together to accomplish a task. The logical flow of data is called a topology.

## WordCountDemo sample application

One of the built-in sample Kafka Streams application is [WordCountDemo](https://github.com/apache/kafka/blob/2.5/streams/examples/src/main/java/org/apache/kafka/streams/examples/wordcount/WordCountDemo.java).

This sample application consumes an input topic, counts how many times words appear, and writes the results back into another topic.

Let's use `WordCountDemo` to count words in our topic `streams-plaintext-input`.

### Must have: download kafka source from https://archive.apache.org/dist/kafka/3.2.1/kafka-3.2.1-src.tgz

Save it as "C:\src\kafka-3.2.1-src".

### Updating WordCountDemo

Unfortunately, `WordCountDemo` is not currently configurable so we will need to make a few small code changes.

### 1. In a text editor, 
open `streams/examples/src/main/java/org/apache/kafka/streams/examples/wordcount/WordCountDemo.java` and make these changes:

```java

package org.apache.kafka.streams.examples.wordcount;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KTable;
import org.apache.kafka.streams.kstream.Produced;

import java.util.Arrays;
import java.util.Locale;
import java.util.Properties;
import java.util.concurrent.CountDownLatch;
import java.io.FileInputStream;
import java.io.IOException;

public final class WordCountDemo {

    public static final String INPUT_TOPIC = "streams-plaintext-input";
    public static final String OUTPUT_TOPIC = "streams-wordcount-output";

    static Properties getStreamsConfig(final String[] args) throws IOException {
		
		final Properties props = new Properties();
		if (args != null && args.length > 0) {
			try (final FileInputStream fis = new FileInputStream(args[0])) {
				props.load(fis);
			}
			if (args.length > 1) {
				System.out.println("Warning: Some command line arguments were ignored. This demo only accepts an optional configuration file.");
			}
		}
        
		props.putIfAbsent(StreamsConfig.APPLICATION_ID_CONFIG, "streams-wordcount");
		props.putIfAbsent(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
		props.putIfAbsent(StreamsConfig.CACHE_MAX_BYTES_BUFFERING_CONFIG, 0);
		props.putIfAbsent(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
		props.putIfAbsent(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());

		// setting offset reset to earliest so that we can re-run the demo code with the same pre-loaded data
		// Note: To re-run the demo, you need to use the offset reset tool:
		// https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Streams+Application+Reset+Tool
		props.putIfAbsent(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
		return props;
	}

    static void createWordCountStream(final StreamsBuilder builder) {
        final KStream<String, String> source = builder.stream(INPUT_TOPIC);

        final KTable<String, Long> counts = source
            .flatMapValues(value -> Arrays.asList(value.toLowerCase(Locale.getDefault()).split(" ")))
            .groupBy((key, value) -> value)
            .count();

        // need to override value serde to Long type
        counts.toStream().to(OUTPUT_TOPIC, Produced.with(Serdes.String(), Serdes.Long()));
    }

    public static void main(final String[] args) {
        //final Properties props = getStreamsConfig();
		
		try{
			
			final Properties props = getStreamsConfig(args);
			final StreamsBuilder builder = new StreamsBuilder();
			createWordCountStream(builder);
			final KafkaStreams streams = new KafkaStreams(builder.build(), props);
			final CountDownLatch latch = new CountDownLatch(1);

			// attach shutdown handler to catch control-c
			Runtime.getRuntime().addShutdownHook(new Thread("streams-wordcount-shutdown-hook") {
				@Override
				public void run() {
					streams.close();
					latch.countDown();
				}
			});
            streams.start();
            latch.await();
		
		}
		catch(IOException e) {
			e.printStackTrace();
        } catch (final Throwable e) {
            System.exit(1);
        }
        System.exit(0);
    }
}

```
<!--
### Looking at the code

This sample application is implemented with the DSL API. The core of the logic lies in the following few lines of codes:

```java
final KStream<String, String> source = builder.stream(INPUT_TOPIC);

final KTable<String, Long> counts = source
    .flatMapValues(value -> Arrays.asList(value.toLowerCase(Locale.getDefault()).split(" ")))
    .groupBy((key, value) -> value)
    .count();

counts.toStream().to(OUTPUT_TOPIC, Produced.with(Serdes.String(), Serdes.Long()));
```

The first line defines the input stream. In this case, it is taking records from our input topic `streams-plaintext-input` and giving us a [KStream](http://kafka.apache.org/25/javadoc/org/apache/kafka/streams/kstream/KStream.html) instance.

The middle statement performs the processing operations. For each record (which is a line in our input file):

    - First, the record value is split by spaces to retrieve all the words.
    - Then, words are grouped together.
    - Finally, it counts how many times each word appear and emit a record `(word, count)` per word.

The last line defines the output stream. Here, we are sending it to our output topic `streams-wordcount-output` and we have to specify a serializer for both the key (words) and the value (current count). -->

### 2. After making these updates done, we need to recompile it. You can do that by running:

Install [gradle](https://gradle.org/install/) and then set the Environment path 

Under "C:\Users\Admin\kafka-3.2.1-src\streams\examples\" run

```sh
gradle assemble
```

### After finishing gradle assemble
```sh
Copy manually the file "kafka-streams-examples-3.2.1.jar" 
from "C:\src\kafka-3.2.1-src\streams\examples\build\libs\" to "C:\kafka_2.13-3.2.1\libs\"
```

### 3. Checking the result

3.1 Create the new topic `streams-plaintext-input`, if you closed it from the part 3.

3.2 We can use a consumer to check the result:

```sh
bin\windows\kafka-console-consumer.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --topic streams-wordcount-output --from-beginning --formatter kafka.tools.DefaultMessageFormatter --property print.key=true --property print.value=true --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer --property value.deserializer=org.apache.kafka.common.serialization.LongDeserializer
```

3.3 Running the WordCountDemo

Start `WordCountDemo` by using `kafka-run-class.bat` and specify our configuration file.

```sh
bin\windows\kafka-run-class.bat org.apache.kafka.streams.examples.wordcount.WordCountDemo
```

3.4 While the Kafka Streams application is running, you can keep adding lines to our file and see new counts being emitted.

3.5 or You can also use a producer to directly write records into the input topic:

```sh
bin\windows\kafka-console-producer.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --topic streams-plaintext-input
```

The Kafka Streams application will run until interrupted, such as by pressing `CTRL+C`.
<!--
The same logic is also implemented using the Processor API, see [WordCountProcessorDemo.java](https://github.com/apache/kafka/blob/trunk/streams/examples/src/main/java/org/apache/kafka/streams/examples/wordcount/WordCountProcessorDemo.java)

## Next Steps

Continue to [workshop summary](../part4/summary.md).-->

back to [part 3](../part3/README.md)

### Alternative to Java --> Python: https://github.com/robinhood/faust (I haven’t tried yet.)
### Gradlew command usage: https://github.com/apache/kafka
### Colab way: https://colab.research.google.com/drive/1rsmLLR1T2o1FANEMbQOGdXlFZ9j6uPfG?usp=sharing

## MAC command

bin/kafka-console-consumer.sh --bootstrap-server "ec2-13-229-46-113.ap-southeast-1.compute.amazonaws.com:9092" --topic streams-wordcount-output --from-beginning --formatter kafka.tools.DefaultMessageFormatter --property print.key=true --property print.value=true --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer --property value.deserializer=org.apache.kafka.common.serialization.LongDeserializer

bin/kafka-console-producer.sh --bootstrap-server "ec2-13-229-46-113.ap-southeast-1.compute.amazonaws.com:9092" --topic streams-plaintext-input

