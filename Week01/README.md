
## Week1 slide and interesting papers

https://docs.microsoft.com/en-us/azure/architecture/data-guide/scenarios/time-series

Lab 1: reading real-time chat from Youtube live (Example of #Ch3ThailandNews)

Python package https://pypi.org/project/pytchat/

<img width="751" alt="Screen Shot 2564-08-11 at 11 50 23" src="https://user-images.githubusercontent.com/69342162/128971375-c60b39a2-0887-40ed-ae19-674cab440160.png">

![image](https://user-images.githubusercontent.com/69342162/151294628-35889347-7a67-43ae-bb2d-5732637ca163.png)
https://towardsdatascience.com/deep-dive-into-netflixs-recommender-system-341806ae3b48

```python
import pytchat
chat = pytchat.create(video_id="oTSzxLvoEJE")
while chat.is_alive():
    for c in chat.get().sync_items():
        print(f"{c.datetime} [{c.author.name}]- {c.message}")
        # write each line to file for kafka connector
```

Lab 2: Twitter stream

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

Good case study: https://www.youtube.com/watch?v=yIFOCYy7Wmc

# Img
<img width="1179" alt="Screen Shot 2565-05-26 at 14 13 19" src="https://user-images.githubusercontent.com/69342162/170437844-97eef492-2ff7-46b1-a714-8e455a19a5d6.png">
Ref: https://www.youtube.com/watch?v=rvqCqK2Lpjg
