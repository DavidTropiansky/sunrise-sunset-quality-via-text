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

# # end
