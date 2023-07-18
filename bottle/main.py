import json

from bottle import route, run, Bottle, response

app = Bottle()


@route('/')
def home():
    response.content_type = 'application/json'
    return json.dumps({'library': 'bottle'})


run(host='localhost', port=8003)
