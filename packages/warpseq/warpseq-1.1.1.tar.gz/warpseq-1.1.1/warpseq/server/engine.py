# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.api.public import Api as WarpApi
from warpseq.server.callbacks import EngineCallbacks
from warpseq.server.packet import CommandPacket
from warpseq.server.model_router import ModelRouter
import time
from multiprocessing.connection import Listener, Client
import json

class WarpBackgroundEngine(object):

    __slots__ = ('_api', '_model_router', 'callbacks', '_listener', '_client')

    def __init__(self, listener=None, client=None):

        api = self._api = WarpApi(web=True)
        api.remove_callbacks()
        self.callbacks = EngineCallbacks(engine=self, song=api.song)
        api.add_callbacks(self.callbacks)
        api.song.edit(tempo=120)

        self._listener = listener
        self._client = client

        self._model_router = ModelRouter(api, self)
        self._model_router.callbacks = self.callbacks

    def loop(self):

        self._api.player.loop(scene=None, infinite=True)

    def check_messages(self):

        while self._listener.poll():
            msg = self._listener.recv()
            msg = json.loads(msg)
            command_packet = CommandPacket.from_dict(msg)
            response_packet = self._model_router.dispatch(msg, command_packet)
            response_data = response_packet.to_json()
            self._client.send(response_data)

def run_engine(init_state):


    address1 = ('localhost', 6001)
    listener = Listener(address1, authkey=b'secret password')

    print("> engine: opening connection")

    with init_state.get_lock():
        init_state.value = 1
    conn = listener.accept()

    print("> engine: web server connected")

    # wait for other side to init listeners

    while True:
        if init_state.value == 2:
            break
        time.sleep(0.05)
    time.sleep(0.5)

    print("> engine: connecting to web server")

    address2 = ('localhost', 6000)
    client = Client(address2, authkey=b'secret password')
    client.send('lets do this')

    with init_state.get_lock():
        init_state.value = 3

    while conn.poll():
        msg = conn.recv()
        print("> engine: %s" % msg)

    engine = WarpBackgroundEngine(listener=conn, client=client)

    devices = engine._api.devices.list()

    if len(devices):
        print("> engine: devices discovered:")
        for (i,x) in enumerate(devices):
            print("> engine: ... %i) %s" % (i,x['name']))

    print("> engine: started event loop")
    engine.loop()

