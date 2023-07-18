from pyramid.config import Configurator
from pyramid.view import view_config


@view_config(route_name='hello', renderer='json')
def hello_world(request):
    return {'library': 'pyramid'}


with Configurator() as config:
    config.add_route('hello', '/')
    config.scan()
    app = config.make_wsgi_app()
from wsgiref.simple_server import make_server

server = make_server('0.0.0.0', 8004, app)
server.serve_forever()
