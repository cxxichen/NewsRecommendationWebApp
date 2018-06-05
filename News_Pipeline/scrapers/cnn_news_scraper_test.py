import cnn_news_scraper as scraper

EXPECTED_STRING = "Here's the official statement from McConnell's office, which doesn't mention the election"
CNN_NEWS_URL = "https://www.cnn.com/2018/06/05/politics/mcconnell-political-rules/index.html"

def test_basic():
    news = scraper.extractNews(CNN_NEWS_URL)

    assert EXPECTED_STRING in news
    print news
    print 'test_basic passed!'

if __name__ ==  "__main__":
    test_basic()
