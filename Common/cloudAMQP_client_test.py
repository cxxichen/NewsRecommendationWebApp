from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://qnfpeoqk:0dCaIiNJQGECRZe1Ot7kFLFNYndKJKuV@spider.rmq.cloudamqp.com/qnfpeoqk"

TEST_QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)
    sentMsg = {'test':'demo'}
    client.sendMessage(sentMsg)
    client.sleep(10)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print 'test_basic passed!'

if __name__ == "__main__":
    test_basic()
