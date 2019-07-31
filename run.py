from __future__ import absolute_import, print_function
import json
import tweepy
import os
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
def func2():
        ckey='**********'  # API key for authentication
        csecret='**********'
        atoken='**********'
        asecret='**********'
        auth=OAuthHandler(ckey,csecret)
        auth.set_access_token(atoken,asecret)
        api=tweepy.API(auth)
        with open(os.path.join('C:\\Users\\parul\\Desktop\\MiniProject\\data.json')) as jfile:
                res=(json.load(jfile))
                print(res)
        """res = requests.get("https://quarkbackend.com/getfile/2013ecs35/pro15")
        res = json.loads(res.text)
        upcoming = res["upcoming"]"""
        upcoming=res["upcoming"]
        tweet = "Next contest: " + upcoming[0]["StartTime"] + " on " + upcoming[0]["Platform"] +". "+ upcoming[0]["url"]+" till " +upcoming[0]["EndTime"]
        api.update_status(status='[TweetPyMail]' + tweet)
        
def main():
        from parseweb import wr
        wr()
        func2()
        from mail import func1
        func1()
      
     
if __name__ == "__main__": main()
