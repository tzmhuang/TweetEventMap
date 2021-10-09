import io
import sys
import numpy as np
import pandas as pd
import itertools
import folium
import re
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PyQt5 import QtWidgets, QtWebEngineWidgets

from twitter_api import *
from language_api import *
from geocoder_api import *
import util

WINDOW_SIZE = (1280, 960)
MAX_ENTITIES = 5
EPS = 0.1


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
        cleaned_tweets = map(
            self.preprocess, [tweet.full_text for tweet in tweets])
        concatenated_tweets = ". ".join(cleaned_tweets)
        try:
            sentiment, magnitude = self._language_api.get_sentiment_from_text(
                concatenated_tweets)
        except:
            sentiment,magnitude = (0,0)
        try:
            entities, _json_entities = self._language_api.get_entities_from_text(
                concatenated_tweets)
        except:
            entities = None
        sentiment = ((sentiment+1)/2)**2*100  # Non-linear transform of [-1, +1] to [0, 100]
        return util.Tweet(concatenated_tweets, geocode, sentiment, magnitude, entities)

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

    def draw_map_plotly(self, center_geocode, tweets):
        lats = [tweet.get_geocode()[0] for tweet in tweets]
        lon = [tweet.get_geocode()[1] for tweet in tweets]
        sentiment = [tweet.get_sentiment() for tweet in tweets]
        magnitude = np.array([tweet.get_magnitude() for tweet in tweets])
        magnitude = magnitude/np.max(magnitude)*100  # Normalize to [0, 100]
        entities = []
        for tweet in tweets:
            try:
                names = list(map(lambda x: x.name, tweet.get_entities()))
                entities += [", ".join(names[0:min(MAX_ENTITIES, len(names))])]
            except:
                print("Error extracting entities")
        hover_text = "<b>Location: (%{lat}, %{lon}) </b><br>" +\
                     "Sentiment: %{z} <br>" + \
                     "Magnitude: %{radius}<br>" + \
                     "Words: %{customdata}<br>"
        fig = go.Figure(go.Densitymapbox(
            lat=lats, lon=lon, z=sentiment, radius=magnitude + EPS*10, customdata=entities, hovertemplate=hover_text))

        fig.update_layout(mapbox_style="open-street-map",
                          mapbox_center_lon=center_geocode.longitude, mapbox_center_lat=center_geocode.latitude,
                          mapbox_zoom=10)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def spin(self, location, method='uniform', **kwargs):
        center = self.get_location_geocodes([location])[0]
        print("Sampling")
        if method == 'uniform':
            grids = self.geocode_sample_uniform(
                location, kwargs['radius'], kwargs['resolution'])
        elif method == 'gaussian':
            grids = self.geocode_sample_gaussian(
                location, kwargs['variance'], kwargs['n_pts'])
        else:
            print("Unknown method")
        print("Done sampling. Processing ... ")
        list_of_tweets = [app.process_tweets_by_geocode(
            coord, 1) for coord in grids]
        if 'save' in kwargs.keys() and kwargs['save']:
            np.save("tweets_UCB_with_mag.npy", list_of_tweets)
        print("Done. Drawing map ...")
        hm = self.draw_map_plotly(center, list_of_tweets)
        print("Done!")
        self.qt = QtWidgets.QApplication(sys.argv)
        w = QtWebEngineWidgets.QWebEngineView()
        w.setHtml(hm.to_html(include_plotlyjs='cdn'))
        w.resize(*WINDOW_SIZE)
        w.show()
        sys.exit(self.qt.exec_())
        return


def get_lat_length(lat):
    # returns the length per latitude in km
    return 111


def get_lon_length(lon, lat):
    # returns the length per longitude in km
    return np.cos(lat*np.pi/180)*get_lat_length(lat)


if __name__ == "__main__":
    app = App()
    app.spin('Times Square, New York City',
             method='uniform', radius=2, resolution=2)
