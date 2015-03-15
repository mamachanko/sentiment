import functools

import gevent
import lymph
from lymph.utils.logging import setup_logger
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

logger = setup_logger(__name__)


class Inbound(lymph.Interface):

    def apply_config(self, config):
        super(Inbound, self).apply_config(config)
        self.stream = self._create_stream(**config.root.get('twitter'))
        self.track_terms = config.root.get('track_terms')

    def _create_stream(self, api_key, api_secret, access_token, access_token_secret): 
        auth = OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)

        listener = TweetStreamListener()
        listener.register_callback(functools.partial(self.emit, 'item.received'))

        return Stream(auth, listener)

    def on_start(self):
        super(Inbound, self).on_start()
        gevent.spawn(self.stream.filter, track=self.track_terms)


class TweetStreamListener(StreamListener):
    
    def __init__(self, *args, **kwargs):
        super(TweetStreamListener, self).__init__(*args, **kwargs)
        self.callbacks = []

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def on_data(self, item):
        logger.debug('item received %s', item)
        for callback in self.callbacks:
            callback(item)

    def on_error(self, status):
        logger.error(status)

