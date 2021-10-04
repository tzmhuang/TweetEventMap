import os
import numpy as np
import pandas as pd
import tweepy
from util import Geocode


N_TWEET = 10


class TweeterAPI():
    def __init__(self):
        consumer_auth = {'consumer_key': os.environ.get('CSM_KEY'),
                         'consumer_secret': os.environ.get('CSM_SCRT')}
        access_auth = {'key': os.environ.get('ACCESS_TKN'),
                       'secret': os.environ.get('ACCESS_SCRT')}
        auth = tweepy.OAuthHandler(**consumer_auth)
        auth.set_access_token(**access_auth)
        self.api = tweepy.API(auth)

    def get_home_timeline(self):
        return self.api.home_timeline()

    def get_tweet_by_geocode(self, geocode, radius, query=None):
        geocode_query = "%s,%s,%skm" % (
            geocode.latitude, geocode.longitude, radius)
        return self.api.search_tweets(q=query, geocode=geocode_query, tweet_mode="extended")


if __name__ == "__main__":
    api = TweeterAPI()

    print("="*20)
    print("Getting Timeline")
    public_tweets = api.get_home_timeline()
    for idx, tweet in enumerate(public_tweets[0:N_TWEET]):
        print(idx, ': ', tweet.text)

    print("="*20)
    print("Searching by Geocode")
    fenway_park = Geocode(42.346268, -71.095764)  # geocode for Fenway Park
    geocode_result = api.get_tweet_by_geocode(fenway_park, 1)
    for idx, tweet in enumerate(geocode_result[0:N_TWEET]):
        print(idx, ': ', tweet.full_text)
