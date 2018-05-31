# -*- coding: utf-8 -*-

import os
import sys
import redis
import hashlib
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24
SLEEP_TIME_IN_SECOUNDS = 10

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://qnfpeoqk:0dCaIiNJQGECRZe1Ot7kFLFNYndKJKuV@spider.rmq.cloudamqp.com/qnfpeoqk"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

redisClient = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQPClient = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
    newsList = news_api_client.getNewsFromSource(NEWS_SOURCES)

    numOfNewNews = 0

    for news in newsList:
        newsDigest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redisClient.get(newsDigest) is None:
            numOfNewNews += 1
            news['digest'] = newsDigest

            if news['publishedAt'] is None:
                # format: YYYY-MM-DDTHH:MM:SS in UTC
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            redisClient.set(newsDigest, news)
            redisClient.expire(newsDigest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQPClient.sendMessage(news)

    print "Fetched %d new news." % numOfNewNews

    cloudAMQPClient.sleep(SLEEP_TIME_IN_SECOUNDS)
