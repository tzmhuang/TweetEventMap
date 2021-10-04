import numpy as np
import pandas as pd
import itertools
import folium
import re
from folium.plugins import HeatMap
import matplotlib.pyplot as plt

from twitter_api import *
from language_api import *
from geocoder_api import *
import util


class App():
    def __init__(self):
        self._twitter_api = TweeterAPI()
        self._language_api = LanguageAPI()
        self._geocoder_api = GeocoderAPI('App')

    def process_tweets_by_geocode(self, geocode, radius):
        # get tweets from geocode
        # join tweets as one long tweet to minimize api call
        # get sentiment from tweet
        # get entities from tweet
        tweets = self._twitter_api.get_tweet_by_geocode(geocode, radius)
        cleaned_tweets = map(self.preprocess, [tweet.full_text for tweet in tweets])
        concatenated_tweets = ". ".join(cleaned_tweets)
        sentiments = self._language_api.get_sentiment_from_text(
            concatenated_tweets)
        entities = self._language_api.get_entities_from_text(
            concatenated_tweets)
        return util.Tweet(concatenated_tweets, geocode, sentiments, entities)

    def geocode_sample_uniform(self, area_name, radius, resolution):
        # radius in km
        n_pts = int(2*radius*resolution)  # number of points across area
        C_pt = self._geocoder_api.get_geocode_by_name(area_name)
        lat_per_km = 1/get_lat_length(C_pt.latitude)
        lon_per_km = 1 / \
            get_lon_length(C_pt.longitude, C_pt.latitude)
        S_bound = C_pt.latitude - lat_per_km*radius
        N_bound = C_pt.latitude + lat_per_km*radius
        E_bound = C_pt.longitude + lat_per_km*radius
        W_bound = C_pt.longitude - lat_per_km*radius
        longitudes = np.linspace(W_bound, E_bound, n_pts)
        latitudes = np.linspace(S_bound, N_bound, n_pts)
        geocodes = map(util.Geocode, np.repeat(
            latitudes, n_pts), np.tile(longitudes, n_pts))
        return list(geocodes)
    
    def geocode_sample_gaussian(self, area_name, variance, n_pts):
        # do sthing
        return

    def get_location_geocodes(self, locations):
        geocodes = []
        for loc in locations:
            geocode = self._geocoder_api.get_geocode_by_name(loc)
            geocodes += [util.Geocode(geocode.latitude, geocode.longitude)]
        return geocodes

    def preprocess(self, text):
        return re.sub(r'http\S+', '', text)

    def draw_map(self, center_geocode, tweets):
        m = folium.Map(location=center_geocode.get_geocode(), zoom_start=12)
        sentiment_data = [tweet.get_geocode()+ [tweet.get_sentiment()] for tweet in tweets]
        HeatMap(sentiment_data).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
        folium.LayerControl().add_to(m)
        return m


def get_lat_length(lat):
    # returns the length per latitude in km
    return 111


def get_lon_length(lon, lat):
    # returns the length per longitude in km
    return np.cos(lat*np.pi/180)*get_lat_length(lat)


if __name__ == "__main__":
    app = App()
    print('='*20)
    print('Checking lat lon calculation')
    print('-'*20)
    fenway = app.get_location_geocodes(['Fenway Park, Boston'])
    print(fenway[0])

    up = get_lat_length(fenway[0].latitude)
    up_lat = 1/up * 200
    up_geocode = Geocode(fenway[0].latitude + up_lat, fenway[0].longitude)
    print(up_geocode)
    print('-'*20)

    left = get_lon_length(fenway[0].longitude, fenway[0].latitude)
    left_lon = 1/left * 200
    left_geocode = Geocode(fenway[0].latitude, fenway[0].longitude - left_lon)
    print(left_geocode)

    print('='*20)
    print('Checking geocode_sample_uniform')
    grids = app.geocode_sample_uniform('Fenway Park, Boston',5, 0.5)
    m = folium.Map(location=fenway[0].get_geocode(), zoom_start=12)
    for pt in grids:
        folium.Marker(pt.get_geocode()).add_to(m)
    m.save("index.html")

    print('='*20)
    print('Checking process_tweets_by_geocode')
    # res = app.process_tweets_by_geocode(fenway[0], 1)
    # print(res)

    print('='*20)
    print('Checking draw_map')
    list_of_tweets = [app.process_tweets_by_geocode(coord, 1) for coord in grids]
    hm = app.draw_map(fenway[0], list_of_tweets)
    hm.save("heatmap.html")


