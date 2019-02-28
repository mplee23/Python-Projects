# api.openweathermap.org

# - Example of API call:
#   api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=dfba918da58c3bb28b54ce6445d97362

"""
Python script to get current temp for a variety of cities
"""

import pandas as pd
import requests
import logging
import time

from read_api_keys import get_api_key


logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

#------------------ CONFIGURATION -------------------------------
api_key = get_api_key('OpenWeather')

# Set your input file here
input_filename = 'C:/Users/LeeMarc-Paul/Downloads/weather cities.txt'

# Set your output file name here.
output_filename = 'C:/Users/LeeMarc-Paul/Downloads/weather current.txt'
# Specify the column name in your input data that contains titles here
city = 'city'
id = 'id'


#------------------ DATA LOADING --------------------------------
# Read the data to a Pandas Dataframe
data = pd.read_table(input_filename, encoding='utf8')

if city not in data.columns:
	raise ValueError('Missing city column in input data')

# Form a list of titles:
# Make a big list of all of the cities to be processed.
cities = data[city].tolist()
ids = data[id].tolist()


#------------------	FUNCTION DEFINITIONS ------------------------
def current_temps(id):
#def current_temps(city):

#   CITY METHOD
#   http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=...
#   weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&APPID=' + api_key

#   ID METHOD
#   http://api.openweathermap.org/data/2.5/weather?id=2172797&APPID=...
   weather_url = 'http://api.openweathermap.org/data/2.5/weather?id=' + str(id) + '&APPID=' + api_key

   # Ping for the reuslts:
   reply = requests.get(weather_url)
   # Results will be in JSON format - convert to dict using requests functionality
   reply = reply.json()
#   code = reply.get('cod')
    
   if len(reply) == 0:
      output = {
        'city' : None
        , 'date' : None
        , 'tempC' : None
        , 'tempF' : None
        , 'maxtempF' : None
      }
                
   else:
      output = {
        'input' : cities[ids.index(int(id))],
        'city' : reply.get('name') + ', ' + reply['sys']['country']
        , 'date' : time.ctime(reply.get('dt'))
        , 'tempC' : str(int(reply['main']['temp'] - 273.15))
        , 'tempF' : str(int((reply['main']['temp'] - 273.15) * 9/5 + 32))
        , 'maxtempF' : str(int((reply['main']['temp_max'] - 273.15) * 9/5 + 32))
      }

   return output



#------------------ PROCESSING LOOP -----------------------------

# Ensure, before we start, that the API key is ok/valid, and internet access is ok
test_result = current_temps('4887398')

if (test_result['city'] != 'Chicago, US'):
    logger.warning('Error with omdb')
    raise ConnectionError('Problem with test results - check the API key and internet connection.')


# Create a list to hold results
results = []

# Go through each title in turn
"""for city in cities:
    temp_result = current_temps(city)
    results.append(temp_result)           
"""
for id in ids:
    temp_result = current_temps(id)
    results.append(temp_result)           

# All done
logger.info('Finished coding all titles')

# Write the full results to csv using the pandas library.
pd.DataFrame(results).sort_values(by='maxtempF', ascending=False).to_csv(output_filename, encoding='utf8', index=False)

