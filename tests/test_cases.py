import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from twitter_api import *
from language_api import *
from geocoder_api import *

def test_twitter_api():
    print("test_twitter_api")
    api = TweeterAPI()
    assert api != None
    print("="*20)
    print("Getting Timeline")
    public_tweets = api.get_home_timeline()
    assert len(public_tweets) > 0

    for idx, tweet in enumerate(public_tweets[0:N_TWEET]):
        print(idx, ': ', tweet.text)

    print("="*20)
    print("Searching by Geocode")
    fenway_park = Geocode(42.346268, -71.095764)  # geocode for Fenway Park
    geocode_result = api.get_tweet_by_geocode(fenway_park, 1)
    assert geocode_result != None
    assert len(geocode_result) > 0
    for idx, tweet in enumerate(geocode_result[0:N_TWEET]):
        print(idx, ': ', tweet.full_text)


def test_language_api():
    print("test_language_api")
    api = LanguageAPI()
    assert api != None

    sample_text = "Hi, this is a test case for language api!.. This is another sentence"
    sentiment, _ = api.get_sentiment_from_text(sample_text)
    assert -1 <= sentiment <= 1

    entities, _ = api.get_entities_from_text(sample_text)
    assert len(entities) > 0

    print("Input: {}".format(sample_text))
    print("Sentiment: {}".format(sentiment))
    print("="*20)
    for entity in entities:
        print("{}, salience: {}, Type: {}".format(entity.name,
              entity.salience, language_v1.Entity.Type(entity.type_).name))


def test_geocoder_api():
    print("test_geocoder_api")
    query = "Fenway Park, Boston"
    api = GeocoderAPI("test_agent")
    assert api != None

    geocode = api.get_geocode_by_name(query)
    assert geocode != None
    print("="*20)
    print("Getting geocode for {}".format(query))
    print("Address: ", geocode.address)
    print("Lon: ", geocode.longitude)
    print("Lat: ", geocode.latitude)