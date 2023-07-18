import json

import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps({"library": "tornado"}))


app = tornado.web.Application([
    (r"/", MainHandler),
])
app.listen(8005)
tornado.ioloop.IOLoop.current().start()
