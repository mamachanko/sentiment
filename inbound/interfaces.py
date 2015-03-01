import functools

import lymph
from lymph.utils.logging import setup_logger
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

logger = setup_logger(__name__)


class Inbound(lymph.Interface, StreamListener):

    def apply_config(self, config):
        super(Inbound, self).apply_config(config)

        api_key = config.root.get('twitter')['api_key']
        api_secret = config.root.get('twitter')['api_secret']
        access_token = config.root.get('twitter')['access_token']
        access_token_secret = config.root.get('twitter')['access_token_secret']

        auth = OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        listener = TweetStreamListener()
        listener.register_callback(functools.partial(self.emit, 'item.received'))

        self.stream = Stream(auth, listener)

    def on_start(self):
        super(Inbound, self).on_start()
        self.stream.filter(track=['pizza'])


class TweetStreamListener(StreamListener):
    
    def __init__(self, *args, **kwargs):
        super(TweetStreamListener, self).__init__(*args, **kwargs)
        self.callbacks = []

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def on_data(self, item):
        logger.info('item received %s', item)
        for callback in self.callbacks:
            callback(item)

    def on_error(self, status):
        logger.error(status)

