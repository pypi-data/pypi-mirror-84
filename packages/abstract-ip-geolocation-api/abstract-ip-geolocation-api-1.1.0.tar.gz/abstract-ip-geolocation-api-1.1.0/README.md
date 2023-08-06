# IP Geolocation for Python (geolocation-api-python)

Python library for Abstract free IP Geolocation API.

Full documentation can be found on Abstract [IP Geolocation API](https://www.abstractapi.com/ip-geolocation-api) page.

## Getting started

Getting started with Abstract IP Geolocation API is very simple, you just need to install the library into your project as follow:

```python
pip install abstract-ip-geolocation-api
```

From there you can then call the geolocationapi as follow:

```python
import abstract-ip-geolocation-api

# Initiate the geolocation api with a free API key retrieved on https://www.abstractapi.com/ip-geolocation-api
geolocation_api = abstract-ip-geolocation-api.v1('YOUR_API_KEY')

# Fetch location data for a given IP
# Note: If you don't provide an ip_address value, then the requester IP will be used
location_data = geolocation_api.geolocate(ip_address="ANY_IP_ADDRESS")

# Process location data and potential errors
if 'ip_address' in location_data:
    # Location data has been successfully retrieved
    country = location_data['country']
    city = location_data['city']
    print(country)
elif 'error' in location_data:
    # Handle Abstract related errors
    error = location_data['error']
    print(error)
else:
    # No location data available for this IP
    print('No location data available for this IP')
```
