from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


class GeocoderAPI():
    def __init__(self, user_agent, rate_limit=1):
        self.rate_limit = rate_limit
        self.user_agent = user_agent
        locator = Nominatim(user_agent=user_agent)
        self.geocode = RateLimiter(
            locator.geocode, min_delay_seconds=rate_limit)

    def get_geocode_by_name(self, query):
        res = self.geocode(query)
        return res


if __name__ == "__main__":
    query = "Fenway Park, Boston"
    # query = "Times Square, New York"
    api = GeocoderAPI("test_agent")
    geocode = api.get_geocode_by_name(query)
    print("="*20)
    print("Getting geocode for {}".format(query))
    print("Address: ", geocode.address)
    print("Lon: ", geocode.longitude)
    print("Lat: ", geocode.latitude)

    
