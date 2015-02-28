import lymph
from lymph.web.interfaces import WebServiceInterface

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response


class Barometer(WebServiceInterface):

    crunching = lymph.proxy('crunching')

    url_map = Map([Rule('/', endpoint='index')])

    def index(self, request):
        avg = self.crunching.avg()
        body_color = self._get_color(avg)
        body = '''
        <html>
            <header>
                <meta http-equiv="refresh" content="1">
            </header>
            <body bgcolor="#%s">
                %s
            </body>
        </html>
        ''' % (body_color, avg)
        return Response(body, content_type='text/html')

    def _get_color(self, avg):
        offset = 255*(1-abs(avg))
        if avg < 0:
            return 'FF%02X00' % offset
        return '%02XFF00' % offset
