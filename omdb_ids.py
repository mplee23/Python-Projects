# http://www.omdbapi.com/?apikey=[yourkey]&

"""
Python script for OMDb
"""

import pandas as pd
import requests
import logging
import time

from read_api_keys import get_api_key

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

#------------------ CONFIGURATION -------------------------------
api_key = get_api_key('OMDB')

# Set your input file here
#input_filename = "C:/Users/LeeMarc-Paul/Downloads/omdb these titles.txt"
input_filename = "C:/Users/LeeMarc-Paul/Downloads/omdb these ids.txt"
# Set your output file name here.
output_filename = "C:/Users/LeeMarc-Paul/Downloads/omdb results.txt"
# Specify the column name in your input data that contains titles here
title = "title"

RETURN_FULL_RESULTS = False

#------------------ DATA LOADING --------------------------------

# Read the data to a Pandas Dataframe
data = pd.read_csv(input_filename, encoding='utf8')

if title not in data.columns:
	raise ValueError("Missing title column in input data")

# Form a list of titles:
# Make a big list of all of the movie titles to be processed.
titles = data[title].tolist()


#------------------	FUNCTION DEFINITIONS ------------------------

def get_omdb_results(title):

#    omdb_url = "http://www.omdbapi.com/?t={}".format(title)+"&apikey={}".format(api_key)
#    USE FOLLOWING FOR IMDB IDS INSTEAD OF TITLES
    omdb_url = "http://www.omdbapi.com/?i={}".format(title)+"&apikey={}".format(api_key)
        
    # Ping omdb for the reuslts:
    results = requests.get(omdb_url)
    # Results will be in JSON format - convert to dict using requests functionality
    results = results.json()
    
#    answer = results['response'][0]
#    answer = results[0]
    output = {
#        "input string" : title,
        "title" : results.get('Title'),
        "year" : results.get('Year'),
        "rated" : results.get('Rated'),
        "released" : results.get('Released'),
        "runtime" : results.get('Runtime'),
        "director" : results.get('Director'),
        "writer" : results.get('Writer'),
        "actors" : results.get('Actors'),
        "language": results.get('Language'),
        "country": results.get('Country'),
        "awards": results.get('Awards'),
        "imdbrating" : results.get('imdbRating'),
        "imdbvotes": results.get('imdbVotes'),
        "imdbID": results.get('imdbID'),
        "type": results.get('Type'),
        "boxoffice": results.get('BoxOffice'),
        "response": results.get('Response')
    }
        
    return output

#------------------ PROCESSING LOOP -----------------------------

# Ensure, before we start, that the API key is ok/valid, and internet access is ok
#test_result = get_omdb_results("The Matrix")
#    USE FOLLOWING FOR IMDB IDS INSTEAD OF TITLES
test_result = get_omdb_results("tt0133093")
if (test_result['response'] != 'True') or (test_result['year'] != '1999'):
    logger.warning("Error with omdb")
    raise ConnectionError('Problem with test results - check the API key and internet connection.')

# Create a list to hold results
results = []
# Go through each title in turn
for title in titles:
    title_result = get_omdb_results(title)
    results.append(title_result)           

# Every 25 titles, save progress to file(in case of a failure so you have something!)
if len(results) % 25 == 0:
    pd.DataFrame(results).to_csv("{}_bak".format(output_filename))


# All done
logger.info("Finished coding all titles")
# Write the full results to csv using the pandas library.
pd.DataFrame(results).to_csv(output_filename, encoding='utf8')
