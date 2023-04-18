# sunrise-sunset-quality-via-text
Small python program that pulls data from sunsetwx.com given a location by user input and texts the user the sunrise/sunset forecast.

To use this program, run the SunsetWxText.py file. 

You will need to sign up for an account with SunsetWx: https://subscriptions.sunsetwx.com/register

As of this writing, the API is free to use for personal use. 

Input the location you would like in the 'loc' variable. This will convert your location into coordinates automatically using 
geopy.geocoders and Nominatim


You will need to sign up for a Twilio account to text you. Twilio gives new users free trial credits, so this app can run free for a while until your credits run out. 
You will need to paste your Twilio SID, auth code, the Twilio provided phone number, and add your personal phone number as the authorzed number to text.



Finally, you can use a service like PythonAnywhere.com to upload your code, and schedule it to run at a certain time everyday. Free accounts on PythonAnywhere can schedule one python program to run on a schedule. If you use python anywhere, make sure to Bash install the required packages on PythonAnywhere.


# Example
```python
from pysunsetwx import PySunsetWx
from twilio.rest import Client



username = '<YOUR sunsetwx USERNAME>'
password = '<YOUR sunsetwx PASSWORD>'

# instantiate PyPexels object
py_sunsetwx = PySunsetWx(username, password)

# Convert location into coordinates
loc = "Central Park, NYC"


from geopy.geocoders import Photon

geolocator = Photon(user_agent="measurements")
location = geolocator.geocode(loc)

lat = location.latitude
lon = location.longitude

print(lat, lon)


# get Quality values for Central Park, NYC
sunrise_lookup = py_sunsetwx.get_quality(lat, lon, 'sunrise')
sunset_lookup = py_sunsetwx.get_quality(lat, lon, 'sunset')


import pprint
pprint.pprint(sunset_lookup)

sunrise_quality = sunrise_lookup['features'][0]['properties']['quality']
sunrise_quality_percent = sunrise_lookup['features'][0]['properties']['quality_percent']
sunrise_validtime_raw = sunrise_lookup['features'][0]['properties']['valid_at']
sunset_validtime_raw = sunset_lookup['features'][0]['properties']['valid_at']
sunset_quality = sunset_lookup['features'][0]['properties']['quality']
sunset_quality_percent = sunset_lookup['features'][0]['properties']['quality_percent']
sunrise_time = sunrise_lookup['features'][0]['properties']['dawn']['astronomical']

from datetime import datetime, timedelta
import pytz


time_string_sunrise = sunrise_validtime_raw 
sunrise_time_object = datetime.strptime(time_string_sunrise, "%Y-%m-%dT%H:%M:%SZ")


time_string_sunset = sunset_validtime_raw 
sunset_time_object = datetime.strptime(time_string_sunset, "%Y-%m-%dT%H:%M:%SZ")



# Create a datetime object from the timestamp for sunrise
dt_sunrise = sunrise_time_object.strftime("%H:%M")

# Create a timezone object for UTC
utc_tz = pytz.timezone('UTC')

# Localize the datetime object to the UTC timezone
dt_sunrise = utc_tz.localize(datetime.strptime(dt_sunrise, '%H:%M')).time()

# create a timezone object for 4 hours ahead
target_tz = pytz.timezone('US/Eastern')

# Convert the datetime object to the target timezone
dt_sunrise = target_tz.normalize(utc_tz.localize(datetime.combine(datetime.today(),dt_sunrise)))
dt_sunrise = dt_sunrise.strftime("%H:%M")




# Create a datetime object from the timestamp sunset
dt_sunset = sunset_time_object.strftime("%H:%M")

# Create a timezone object for UTC
utc_tz = pytz.timezone('UTC')

# Localize the datetime object to the UTC timezone
dt_sunset = utc_tz.localize(datetime.strptime(dt_sunset, '%H:%M')).time()

# create a timezone object for 4 hours ahead
target_tz = pytz.timezone('US/Eastern')

# Convert the datetime object to the target timezone
dt_sunset = target_tz.normalize(utc_tz.localize(datetime.combine(datetime.today(),dt_sunset)))
dt_sunset = dt_sunset.strftime("%H:%M")



message = f'The sun forecast for tomorrow at {loc} will be as follows: Sunrise quality tomorrow will be {sunrise_quality} ({sunrise_quality_percent}%) at {dt_sunrise}. Sunset quality today will be {sunset_quality} ({sunset_quality_percent}%) at {dt_sunset}.'
print(message)


#Sending the text message


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = '<YOUR TWILIO ACCOUNT SID>'
auth_token = '<YOUR TWILIO ACCOUNT TOKEN>'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+<YOUR TWILIO PHONE NUMBER>',
                              body=message,
                              to='+<PHONE NUMBER YOU WANT TO TEXT>'
                          )



# OUTPUT: 
# 40.7827725 -73.9653627406542
# {'features': [{'geometry': {'coordinates': [-73.9783, 40.777], 'type': 'Point'},
#               'properties': {'distance': 1.264,
#                              'dusk': {'astronomical': '2023-01-13T23:28:00Z',
#                                       'civil': '2023-01-13T22:21:00Z',
#                                       'nautical': '2023-01-13T22:55:00Z'},
#                             'imported_at': '2023-01-13T14:32:34Z',
#                              'last_updated': '2023-01-13T12:00:00Z',
#                              'quality': 'Poor',
#                              'quality_percent': 21.0,
#                              'quality_value': -288.41,
#                              'source': 'NAM',
#                              'temperature': 4.35,
#                              'type': 'Sunset',
#                              'valid_at': '2023-01-13T21:51:00Z'},
#               'type': 'Feature'}],
# 'type': 'FeatureCollection'}
# The sun forecast for tomorrow at Central Park, NYC will be as follows: Sunrise quality tomorrow will be Poor (16.94%) at 07:18. Sunset quality today will be Poor (21.0%) at 16:51.
```

<img width="361" alt="image" src="https://user-images.githubusercontent.com/113219225/212402403-4d3b73da-39da-4729-9660-4a4df8b0a383.png">
