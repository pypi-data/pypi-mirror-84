# ------------------------------------------------------------------
# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# this implements the public Python API for WarpSeq.
# see examples/api/*.py for usage. Direct access to model
# objects through other means is not a "supported" or stable API contract.

import gc
import random
import json

from warpseq.api.interfaces.devices import Devices
from warpseq.api.interfaces.instruments import Instruments
from warpseq.api.interfaces.patterns import Patterns
from warpseq.api.interfaces.transforms import Transforms
from warpseq.api.interfaces.player import Player
from warpseq.api.interfaces.scales import Scales
from warpseq.api.interfaces.scenes import Scenes
from warpseq.api.interfaces.song import SongApi
from warpseq.api.interfaces.tracks import Tracks
from warpseq.api.interfaces.clips import Clips
from warpseq.api.interfaces.data_pools import DataPools
from warpseq.playback import midi
from warpseq.model.song import Song
from warpseq.api.callbacks import Callbacks, DefaultCallbacks

gc.disable()

MIDI_PORTS = midi.get_devices()

class Api(object):

    __slots__ = ( '_song', 'song', 'devices', 'instruments', 'scales',
                  'patterns', 'data_pools', 'transforms', 'scenes', 'tracks', 'clips',
                  'player', 'song', '_callbacks', 'web' )

    def __init__(self, default_callbacks=True, web=False):

        random.seed()
        self.web = web

        self._callbacks = Callbacks()
        if default_callbacks:
            self._callbacks.clear()
            self._callbacks.register(DefaultCallbacks())

        self._song = Song(name='')

        self.song = SongApi(self, self._song)

        self.devices = Devices(self, self._song)
        self.instruments = Instruments(self, self._song)
        self.scales = Scales(self, self._song)
        self.patterns = Patterns(self, self._song)
        self.data_pools = DataPools(self, self._song)
        self.transforms = Transforms(self, self._song)
        self.scenes = Scenes(self, self._song)
        self.tracks = Tracks(self, self._song)
        self.clips = Clips(self, self._song)

        self.player = Player(self, self._song)

        if web:
            self.extra_setup()

    def remove_callbacks(self):
        self._callbacks.clear()

    def add_callbacks(self, cb):
        self._callbacks.register(cb)

    def reset(self, init=True):
        self.player.stop()
        self._song.reset(clear=True)
        if init and self.web:
           self.extra_setup()

    def extra_setup(self):
        random.seed()
        self.scales.add(name='s1', note='C', octave=0, scale_type='major')
        for x in range(1,5):
            self.scenes.add(name='Scene %s' % x)
            self.tracks.add(name='Track %s' % x, instruments=[])

    def from_dict(self, data):
        self.reset(init=False)
        self._song.load_from_dict(data)
        self.devices.auto_add_discovered()

    def to_dict(self):
        return self._song.to_dict()

    def from_json(self,  data):
        data = json.loads(data)
        return self.from_dict(data)

    def to_json(self):
        return self._song.to_json()
