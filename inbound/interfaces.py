import functools
import json

import gevent
import lymph
from lymph.utils.logging import setup_logger
import tweepy

logger = setup_logger(__name__)


class Inbound(lymph.Interface):

    def apply_config(self, config):
        super(Inbound, self).apply_config(config)
        self.auth = self._create_auth(**config.root.get('twitter'))
        self.stream = self._create_stream(self.auth)
        self.api = tweepy.API(self.auth)
        self.track_terms = config.root.get('track_terms')

    def _create_auth(self, api_key, api_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

    def _create_stream(self, auth): 
        listener = TweetStreamListener()
        listener.register_callback(self.tweet_received)
        return tweepy.Stream(auth, listener)

    def tweet_received(self, tweet):
        tweet = json.loads(tweet) 
        oembed = self.api.get_oembed(
            tweet['id'],
            hide_media=True,
            hide_thread=True,
            omit_script=1
        )
        tweet['html'] = oembed['html']
        logger.info('tweet received %s...', str(tweet)[:150])
        self.emit('tweet.received', json.dumps(tweet))

    def on_start(self):
        super(Inbound, self).on_start()
        gevent.spawn(self.stream.filter, track=self.track_terms)


class TweetStreamListener(tweepy.streaming.StreamListener):
    
    def __init__(self, *args, **kwargs):
        super(TweetStreamListener, self).__init__(*args, **kwargs)
        self.callbacks = []

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def on_data(self, tweet):
        for callback in self.callbacks:
            callback(tweet)

    def on_error(self, status):
        logger.error(status)

