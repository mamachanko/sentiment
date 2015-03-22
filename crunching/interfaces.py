import json

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import lymph


class Crunching(lymph.Interface):

    def on_start(self):
        super(Crunching, self).on_start()
        self.es = Elasticsearch(hosts='es')

    @lymph.rpc()
    def avg(self):
        search = Search(using=self.es, index='tweets')
        search.aggs.bucket('avg_sentiment', 'avg', field='sentiment')
        response = search.execute()
        return response.aggregations['avg_sentiment']['value']

    @lymph.rpc()
    def count(self):
        search = Search(using=self.es, index='tweets')
        search.execute()
        return search.count()

    @lymph.rpc()
    def recent(self, limit=5):
        search = Search(using=self.es, index='tweets', extra={"size": limit})
        search = search.sort('-timestamp_ms')
        result = search.execute()
        return map(lambda item: item.to_dict(), result)
