# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from wsgiref import simple_server
import falcon
import os
import json
import sys

from warpseq.server.packet import CommandPacket
from warpseq.api.public import Api as WarpApi
from warpseq.server.templar import Templar
from warpseq.server.page_builder import PageBuilder
from warpseq.api.exceptions import TimeoutException
from multiprocessing.connection import Listener, Client
import time
from wsgiref.simple_server import WSGIRequestHandler

#=======================================================================================================================

class BaseResource(object):

    __slots__ = ('mailbox', 'listener', 'client')

    def __init__(self, listener=None, client=None):

        self.listener = listener
        self.client = client

    def _send_to_engine(self, data):

        self.client.send(json.dumps(data))
        msg = self.listener.recv()
        return msg

# ======================================================================================================================

class ModelResource(BaseResource):

    __slots__ = ()

    def on_post(self, req, resp):

        data = CommandPacket.from_dict(req.media).to_dict()

        try:

            out = self._send_to_engine(data)

            data_out = json.loads(out)

            if not data_out['ok']:

                resp.status = falcon.HTTP_500

            resp.media = data_out

        except TimeoutException:
            resp.status = falcon.HTTP_500
            resp.media = dict(timeout=True)

# ======================================================================================================================

class IndexResource(object):

    __slots__ = ('path',)

    def __init__(self, path=None):
        self.path = path

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        filename = os.path.join(self.path, 'index.html')
        with open(filename, 'r') as f:
            resp.body = f.read()

# ======================================================================================================================

class PagesResource(BaseResource):

    __slots__ = ('templar', 'pages')

    def __init__(self, templar=None, listener=None, client=None):
        self.templar = templar
        super().__init__(listener=listener, client=client)
        self.pages = PageBuilder(templar=templar, listener=listener, client=client)

    def on_get(self, req, resp, category, item):
        resp.status = falcon.HTTP_200
        resp.body = self.pages.render(category, item)

# ======================================================================================================================


class DontLog(WSGIRequestHandler):

    def log_message(self, format, *args):
        pass


def run_server(host='127.0.0.1', port=8000, init_state=None):

    app = falcon.API()

    p = os.path.abspath(sys.modules[WarpApi.__module__].__file__)
    p = os.path.dirname(os.path.dirname(p))

    static_path = os.path.join(p, 'static')
    template_path = os.path.join(p, 'templates')
    templar = Templar(template_path)

    # wait for engine to say it is ready for connections
    print("> web server: waiting for engine")
    while True:
        if init_state.value == 1:
            break
        time.sleep(0.05)
    time.sleep(0.5)
    print("> web server: connecting to engine")

    address2 = ('localhost', 6001)
    client = Client(address2, authkey=b'secret password')
    client.send('whazzup')

    address1 = ('localhost', 6000)
    listener = Listener(address1, authkey=b'secret password')

    print("> web server: ready for engine connection")

    with init_state.get_lock():
        init_state.value = 2
    conn = listener.accept()

    print("> web server: engine connected")
    while conn.poll():
        msg = conn.recv()
        print("> webserver: %s" % msg)

    app.add_route('/', IndexResource(static_path))
    app.add_route('/model', ModelResource(listener=conn, client=client))
    app.add_route('/pages/{category}/{item}', PagesResource(templar=templar, listener=conn, client=client))
    app.add_static_route('/static', static_path)

    print("> webserver ready at http://%s:%s/" % (host, port))

    try:
        httpd = simple_server.make_server(host, port, app, handler_class=DontLog)
    except OSError as oe:
        if oe.errno == 48:
            sys.stderr.write("\n\naddress is already in use\n\n")
        raise

    httpd.serve_forever()


