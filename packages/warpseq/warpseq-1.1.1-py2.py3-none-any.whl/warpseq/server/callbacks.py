# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.api.callbacks import BaseCallbacks
from warpseq.server.packet import ResponsePacket
from warpseq.api.exceptions import StopException
import json

class EngineCallbacks(BaseCallbacks):

    __slots__ = ('engine','mailbox','song')

    def __init__(self, engine=None, song=None):
        self.engine = engine
        self.song = song

    def on_scene_start(self, scene):

        self._handle_messages();

    def on_clip_start(self, clip):
        print(">> starting clip: %s (%s)" % (clip.name, clip.obj_id))
        pass

    def on_clip_stop(self, clip):
        print(">> stopping clip: %s (%s)" % (clip.name, clip.obj_id))
        pass

    def on_clip_restart(self, clip):
        print(">> restarting clip: %s (%s)" % (clip.name, clip.obj_id))
        pass

    def on_pattern_start(self, clip, pattern):
        print(">> starting pattern: %s (%s)/%s (%s)" % (clip.name, clip.obj_id, pattern.name, pattern.obj_id))
        pass

    def all_clips_done(self):
        print(">> all clips done")

    def keyboard_interrupt(self):
        print(">> keyboard interrupt")

    def on_multiplayer_advance(self):
        self._handle_messages()

    def _handle_messages(self):
        self.engine.check_messages()

