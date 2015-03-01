import json

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import lymph
from textblob import TextBlob


class Crunching(lymph.Interface):

    def on_start(self):
        super(Crunching, self).on_start()
        self.es = Elasticsearch(hosts='es')

    @lymph.event('item.received')
    def ingest(self, event):
        item = json.loads(event.body)
        item['sentiment'] = self._get_sentiment(item['text'])
        self.es.index(index='items', doc_type='item', body=item)

    def _get_sentiment(self, text):
        text_blob = TextBlob(text)
        return text_blob.sentiment.polarity

    @lymph.rpc()
    def avg(self):
        search = Search(using=self.es, index='items')
        search.aggs.bucket('avg_sentiment', 'avg', field='sentiment')
        response = search.execute()
        return response.aggregations['avg_sentiment']['value']

    @lymph.rpc()
    def count(self):
        search = Search(using=self.es, index='items')
        search.execute()
        return search.count()
