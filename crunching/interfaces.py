import json

from elasticsearch import Elasticsearch
import lymph
from textblob import TextBlob


class Crunching(lymph.Interface):

    def on_start(self):
        super(Crunching, self).on_start()
        self.es = Elasticsearch(hosts='es')

    @lymph.event('data.received')
    def digest(self, event):
        data = json.loads(event.body)
        data['sentiment'] = self._get_sentiment(data['text'])
        self.es.index(index='sentiments', doc_type='sentiment-type', body=data)

    def _get_sentiment(self, text):
        text_blob = TextBlob(text)
        return text_blob.sentiment.polarity

    @lymph.rpc()
    def avg(self):
        result = self.es.search(
            index='sentiments',
            body={"aggs" : {"avg_sentiment" : {"avg" : {"field" : "sentiment"}}}}
        )
        return result['aggregations']['avg_sentiment']['value']

    @lymph.rpc()
    def count(self):
        return self.es.count(index='sentiments', doc_type='sentiment-type')['count']
 
