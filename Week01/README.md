## Week1 slide
![image](https://user-images.githubusercontent.com/69342162/173461061-bfca49fc-f49f-4dce-94da-c88c1325ed65.png)

<!--![image](https://user-images.githubusercontent.com/69342162/173226832-e3c42a60-72b2-4402-bd64-60a3004eb357.png)-->

<!--![image](https://user-images.githubusercontent.com/69342162/171875698-48b20d55-e6ea-4f7b-a987-df779031dc0f.png) -->


### Lab 1: reading real-time chat from Youtube live (Example of #Ch3ThailandNews)

Python package https://pypi.org/project/pytchat/

<img width="751" alt="Screen Shot 2564-08-11 at 11 50 23" src="https://user-images.githubusercontent.com/69342162/128971375-c60b39a2-0887-40ed-ae19-674cab440160.png">

```python
import pytchat
chat = pytchat.create(video_id="oTSzxLvoEJE")
while chat.is_alive():
    for c in chat.get().sync_items():
        print(f"{c.datetime} [{c.author.name}]- {c.message}")
        # write each line to file for kafka connector
```

### Lab 2: Twitter stream

``` python
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

class listener(StreamListener):
    
    def on_data(self, data):
      	print (data.encode().decode('unicode_escape'))
      	return True
    
    def on_error(self, status):
        print (status)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["popcat"])
```
### Todo
1. Modify the slide by adding the images from this website, including big data, batch, and real-time processing
2. https://docs.microsoft.com/en-us/azure/architecture/data-guide/big-data/
3. Add "redash" for visualization from druid
4. Add "sparkml" or other tech like river, vopal wabbit (https://booking.ai/crunching-big-data-with-4-machine-learning-libraries-284ae3167885), https://mlcourse.ai/book/topic08/topic08_intro.html in betwee spark stream and druid.

### Reference (Must read)
- https://huyenchip.com/2020/12/27/real-time-machine-learning.html
- https://www.confluent.io/learn/data-streaming/
- https://medium.com/@chandanbaranwal/spark-streaming-vs-flink-vs-storm-vs-kafka-streams-vs-samza-choose-your-stream-processing-91ea3f04675b

### Dataset
- https://moa.cms.waikato.ac.nz/datasets/
- https://www.jigsawacademy.com/blogs/ai-ml/time-series-dataset
