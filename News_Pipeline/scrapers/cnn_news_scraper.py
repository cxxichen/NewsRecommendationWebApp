import os
import random
import requests

from lxml import html

GET_CNN_NEWS_XPATH = '''//p[@class='zn-body__paragraph speakable']//text() | //div[@class='zn-body__paragraph speakable']//text() | //div[@class='zn-body__paragraph']//text()'''


# Load user agents
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []


with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])
random.shuffle(USER_AGENTS)


def getHeaders():
    userAgent = random.choice(USER_AGENTS)
    headers = {
        "Connection" : "close",
        "User-Agent" : userAgent
    }
    return headers


def extractNews(newsUrl):
    # Fetch HTML
    sessionRequest = requests.session()
    response = sessionRequest.get(newsUrl, headers=getHeaders())

    news = {}

    try:
        # Parse html
        tree = html.fromstring(response.content)
        # Extract information
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
    except Exception as e:
        print # coding=utf-8
        return {}

    return news
