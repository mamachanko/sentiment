import os
from operator import itemgetter

import lymph
from lymph.utils.logging import setup_logger
from lymph.web.interfaces import WebServiceInterface
import pystache
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response

logger = setup_logger(__name__)


class Barometer(WebServiceInterface):
    crunching = lymph.proxy('crunching', timeout=.75)

    url_map = Map([
        Rule('/', endpoint='index'),
        Rule('/static/<path:path>', endpoint='static'),
    ])

    def index(self, request):
        template = self._read_resource('index.html').decode('utf8')
        renderer = pystache.Renderer(escape=lambda u: u)
        body = renderer.render(template, self._get_content())
        return Response(body, content_type='text/html')

    def _get_content(self):
        try:
            count = self.crunching.count()
            avg = self.crunching.avg()
        except (lymph.LookupFailure, lymph.Timeout):
            count = 'unkown'
            avg = 'unkown'
            color = 'FFFFFF'
        else:
            color = self._get_color(avg)
            avg = '%.4f' % avg
        return {'color': color,
                'avg': avg,
                'count': count,
                'tweets': self._get_tweets()}

    def _get_color(self, avg):
        offset = 255*(1-abs(avg))
        if avg < 0:
            return 'FF%02X00' % offset
        return '%02XFF00' % offset

    def _get_tweets(self):
        try:
            tweets = self.crunching.recent()
        except (lymph.LookupFailure, lymph.Timeout):
            return 'failed looking up tweets'
        else:
            html = map(itemgetter('html'), tweets)
            return u''.join(html)

    def static(self, request, path):
        if path.startswith('css'):
            content_type = 'text/css'
        else:
            content_type = 'image/png'
        content = self._read_resource(request.path)
        return Response(content, content_type=content_type)

    def _read_resource(self, path):
        path = path.lstrip('/')
        current_dir = os.path.dirname(os.path.abspath(__file__))
        resource_path = os.path.join(current_dir, path)
        logger.debug('reading resource %s', resource_path)
        with open(resource_path) as resource:
            return resource.read()
