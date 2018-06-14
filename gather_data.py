from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import logging
import logging.handlers
import json
import evaluator
import bm25.bm25_result_parser as rparser

consumer_key = "ZN3oupo3WzZmIcvNSGXdK4yea"
consumer_secret = "wZwscKyJc60xizrSSWNKRhRrllRLYyv7RpKWKVsCiPHfuGghAp"
access_token = "873881805119672322-MyeCpCteUIUzjKmHGBB5ZPcbp8mMVqZ"
access_token_secret = "PatrEqAWDPDe53PnLJEuvMsqQ7fycI76SppkKnJQcuajM"

# tweets_file = open('data.json','w')
tweets_list = []
i = 0


class TweetListener(StreamListener):
    def __init__(self, api=None):
        super(TweetListener, self).__init__(api)
        self.logger = logging.getLogger('tweetlogger')

        statusHandler = logging.handlers.TimedRotatingFileHandler('status.log', when='H', encoding='bz2', utc=True)
        statusHandler.setLevel(logging.INFO)
        self.logger.addHandler(statusHandler)

        warningHandler = logging.handlers.TimedRotatingFileHandler('warning.log', when='H', encoding='bz2', utc=True)
        warningHandler.setLevel(logging.WARN)
        self.logger.addHandler(warningHandler)
        logging.captureWarnings(True)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.WARN)
        self.logger.addHandler(consoleHandler)

        self.logger.setLevel(logging.INFO)
        self.count = 0

    def on_data(self, data):
        self.count += 1
        self.logger.info(data)

        global tweets_list
        #    tweets_list.append(json.dumps(data))
        tweets_list.append(data)
        if self.count % 100 == 0:
            print "%d statuses processed" % self.count
            #        print tweets_list
            global i
            i = i % 10
            with open(str(i) + '_temp_tweet.txt', 'w') as f:
                f.write(json.dumps(tweets_list))
            bulk_tweet(i)
            i = i + 1
            # print i
            # bulk_tweet()
            tweets_list = []

        # it will call evaluate_for_thresold function after defined count.
        # if self.count % 40000 == 0:
        #     rparser.evaluate_for_thresold(8, 205)
        # return True

    def on_error(self, exception):
        self.logger.warn(str(exception))


def bulk_tweet(i):
    evaluator.set_data(i)


def start_tweets_api():
    listener = TweetListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)
    while True:
        try:
            stream.sample(languages=['en'])
            # stream.filter(track=["Narendra Modi","PMModi","Modi"])
        except Exception as ex:
            print str(ex)