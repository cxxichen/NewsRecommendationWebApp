import requests
from json import loads

NEWS_API_ENDPOINT = 'https://newsapi.org/v2/'
API_KEY = '305bb298c1994f2ebb09c938081cc1c6'
API = 'everything'

CNN = 'cnn'
DEFAULT_SOURCES = [CNN]

def buildUrl(end_point=NEWS_API_ENDPOINT, api_name=API):
    return end_point + api_name

def getNewsFromSource(sources=DEFAULT_SOURCES):
    articles = []
    for source in sources:
        payload = {
            'apiKey' : API_KEY,
            'sources' : source
        }
        response = requests.get(buildUrl(), params=payload)
        res_json = loads(response.content)

        # Extract info from response
        if (res_json is not None and res_json['status'] == 'ok'):
            articles.extend(res_json['articles'])
    return articles
