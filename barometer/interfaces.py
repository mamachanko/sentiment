import os

import lymph
from lymph.utils.logging import setup_logger
from lymph.web.interfaces import WebServiceInterface
import pystache
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response

logger = setup_logger(__name__)


class Barometer(WebServiceInterface):

    crunching = lymph.proxy('crunching')

    url_map = Map([
        Rule('/', endpoint='index'),
        Rule('/static/<path:path>', endpoint='static'),
    ])

    def index(self, request):
        count = self.crunching.count()
        avg = self.crunching.avg()
        template = self._read_resource('index.html').decode('utf8')
        body = pystache.render(
            template,
            {'color': self._get_color(avg), 'avg': avg, 'count': count}
        )
        return Response(body, content_type='text/html')

    def static(self, request, path):
        if path.startswith('css'):
            content_type = 'text/css'
        else:
            content_type = 'image/png'
        content = self._read_resource(request.path)
        return Response(content, content_type=content_type)

    def _get_color(self, avg):
        offset = 255*(1-abs(avg))
        if avg < 0:
            return 'FF%02X00' % offset
        return '%02XFF00' % offset

    def _read_resource(self, path):
        path = path.lstrip('/')
        current_dir = os.path.dirname(os.path.abspath(__file__))
        resource_path = os.path.join(current_dir, path)
        logger.debug('reading resource %s', resource_path)
        with open(resource_path) as resource:
            return resource.read()
