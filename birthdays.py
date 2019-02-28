"""
Python IN PROGRESS to query Google Knowledge Graph
https://developers.google.com/knowledge-graph/

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
#Google KnowledgeBase key
api_key = get_api_key('KG')

# KGSearchWidget(<API_KEY>, document.getElementById("myInput"), {});

# Set your input file here

# Set your output file name here.

# Specify the column name in your input data that contains titles here


RETURN_FULL_RESULTS = False

#SAMPLE----------------------------------------------------------
"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib
import urllib3

query = 'Taylor Swift'
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
params = {
    'query': query,
    'limit': 10,
    'indent': True,
    'key': api_key,
}
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())
#for element in response['itemListElement']:
#  print element['result']['name'] + ' (' + str(element['resultScore']) + ')'


