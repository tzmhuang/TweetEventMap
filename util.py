
class Tweet():
    def __init__(self, text, geocode, sentiment, magnitude, entities):
        self._text = text
        self._geocode = geocode
        self._sentiment = sentiment
        self._magnitude = magnitude
        self._entities = entities

    def get_text(self):
        return self._text

    def get_geocode(self):
        return self._geocode.get_geocode()

    def get_sentiment(self):
        return self._sentiment
    
    def get_magnitude(self):
        return self._magnitude

    def get_entities(self):
        return self._entities

    def __str__(self):
        return ('Tweet(text=' + self._text
                + ', geocode=' + self._geocode.__str__()
                + ', sentiment: ' + self._sentiment.__str__()
                + ', entities: ' + self._entities.__str__())


class Geocode():
    def __init__(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude
    
    def get_geocode(self):
        return [self.latitude, self.longitude]

    def __str__(self):
        return 'Geocode(latitude=%s, longitude=%s)' % (self.latitude, self.longitude)
