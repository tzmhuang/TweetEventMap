import os
import numpy as np
import pandas as pd
import tweepy

N_TWEET = 10

class TweeterAPI():
    def __init__(self, auth):
        self.api = tweepy.API(auth)

    def get_home_timeline(self):
        return self.api.home_timeline()
    
    def get_tweet_by_geocode(self, geocode, query = None):
        return self.api.search_tweets(q=query   , geocode=geocode)


if __name__ == "__main__":
    consumer_auth = {'consumer_key': os.environ.get('CSM_KEY'),
                     'consumer_secret': os.environ.get('CSM_SCRT')}

    access_auth = {'key': os.environ.get('ACCESS_TKN'),
                   'secret': os.environ.get('ACCESS_SCRT')}
    print(consumer_auth)
    print(access_auth)
    auth = tweepy.OAuthHandler(**consumer_auth)
    auth.set_access_token(**access_auth)
    api = TweeterAPI(auth)

    print("="*20)
    print("Getting Timeline")
    public_tweets = api.get_home_timeline()
    for idx, tweet in enumerate(public_tweets[0:N_TWEET]):
        print(idx,': ' ,tweet.text)

    print("="*20)
    print("Searching by Geocode")
    geocode_result = api.get_tweet_by_geocode("42.346268,-71.095764,1mi") # geocode for Fenway Park
    for idx, tweet in enumerate(geocode_result[0:N_TWEET]):
        print(idx, ': ', tweet.text)

