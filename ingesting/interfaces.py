import json

from elasticsearch import Elasticsearch
import lymph
from textblob import TextBlob


class Ingesting(lymph.Interface):

    def on_start(self):
        super(Ingesting, self).on_start()
        self.es = Elasticsearch(hosts='es')

    @lymph.event('tweet.received')
    def ingest(self, event):
        tweet = json.loads(event.body)
        tweet['sentiment'] = self._get_sentiment(tweet['text'])
        self.es.index(index='tweets', doc_type='tweet', body=tweet)

    def _get_sentiment(self, text):
        text_blob = TextBlob(text)
        return text_blob.sentiment.polarity
