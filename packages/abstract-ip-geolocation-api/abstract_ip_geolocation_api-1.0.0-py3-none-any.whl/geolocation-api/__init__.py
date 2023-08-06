import requests
import json

class v1:

    def __init__(self, api_key):
        self.api_key = api_key

    def geolocate(self, ip_address=""):
        url = 'https://ipgeolocation.abstractapi.com/v1/?'

        params = {
            'api_key': self.api_key
        }

        if ip_address:
            params['ip_address'] = ip_address

        response = requests.get(url, params=params)

        if response.status_code == 204:
            # Returning empty json since no location data found
            data = {}
        else:
            data = response.json()

        return data