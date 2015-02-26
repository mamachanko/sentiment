import lymph
from lymph.web.interfaces import WebServiceInterface

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response


class Barometer(WebServiceInterface):

    crunching = lymph.proxy('crunching')

    url_map = Map([Rule('/', endpoint='index')])

    def index(self, request):
        avg = self.crunching.avg()
        body_color = 'ff0000'
        body = '<html><header><meta http-equiv="refresh" content="1"></header><body bgcolor="#%s">%s</body></html>' % (body_color, avg)
        return Response(body, content_type='text/html')
