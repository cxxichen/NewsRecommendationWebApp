# -*- coding: utf-8 -*-

import os
import sys

from goose import Goose

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

# Use my own Cloud AMQP queue
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://kbcfxixs:YNAGcD02Y3TCh4iMyFlgLYm8swew7pHD@baboon.rmq.cloudamqp.com/kbcfxixs"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://qnfpeoqk:0dCaIiNJQGECRZe1Ot7kFLFNYndKJKuV@spider.rmq.cloudamqp.com/qnfpeoqk"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return

    task = msg

    g = Goose()
    article = g.extract(url=task['url'])

    # print article.cleaned_text

    task['text'] = article.cleaned_text

    # # Scraping CNN news
    # text = None
    # if task['source']['id'] == 'cnn':
    #     print "Scraping CNN news"
    #     text = cnn_news_scraper.extractNews(task['url'])
    # else:
    #     print "News source [%s] is not supported." % task['source']['name']
    #
    # task['text'] = text

    dedupe_news_queue_client.sendMessage(task)

while True:
    # fetch msg from queue
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Handle message
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
