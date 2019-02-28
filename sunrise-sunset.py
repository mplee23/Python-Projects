import requests
import time
import datetime, pytz
from geopy.geocoders import GoogleV3

Google_KEY = 'AIzaSyD21VtnS4pR164YKIdmWOKMOlaQ3NPfaxo'
#Weather_KEY = 'dfba918da58c3bb28b54ce6445d97362'
Weather_KEY = 'cdcba84181ab6028a0c8cb04b609463c'

####LOCATION####
city = str(input('City name: '))
country = str(input('Country name: '))  #get user input for location

####GEOPY####
# g = GoogleV3()  #use googleV3 engine as it allows for predictive queries (can misspell inputs and will still generally return a result) and for timezone identification
g = GoogleV3(api_key=Google_KEY)

print('Location : {}, {}'.format(city, country))



location = g.geocode(query='{}, {}'.format(city, country))

print(location)

####PYTZ####

utcOffset = datetime.datetime.now(pytz.timezone(str(g.timezone(location.point))))  #find timezone offset(openweathermap returns sunrise and sunset values in UTC time) which must be added to sunrise and sunset times

timezoneEpoch = int(utcOffset.utcoffset().total_seconds())


####MAIN####
#use openweathermap due to its easy to use API and generous free tier
url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID=' + Weather_KEY + '.format(location.latitude, location.longitude)'  

resp = requests.get(url).json()

sunrise = int('{}'.format(resp['sys']['sunrise'])) + timezoneEpoch
sunset = int('{}'.format(resp['sys']['sunset'])) + timezoneEpoch

sunriseTime = time.strftime('%H:%M:%S', time.localtime(sunrise))
sunsetTime = time.strftime('%H:%M:%S', time.localtime(sunset))

print('Sunrise: {} \nSunset: {}\n'.format(sunriseTime, sunsetTime))
