# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# the multi-player class contains high level methods for playing
# clips and scenes, as such the individual (track-specific) interface,
# player.py, is a less public API than this one.

import ctypes
import time

from ..api.callbacks import Callbacks
from ..model.base import BaseObject
import time
import gc
import asyncio

LONG_WAIT = 50 / 1000
# SHORT_WAIT = 1 / 8000
MILLISECONDS = 2

async def zsleep(xtime):
    await asyncio.sleep(xtime/1000.0)

class MultiPlayer(object):

    __slots__ = [ 'song', 'engine_class', 'clips', 'players', 'callbacks', 'stop_if_empty', 'stopped', 'started']

    def __init__(self, song=None, engine_class=None, stop_if_empty=True):
        self.song = song
        self.engine_class = engine_class
        self.callbacks = Callbacks()
        self.stop_if_empty = stop_if_empty
        self.reset()

    def reset(self):
        self.clips = []
        self.players = {}
        self.stopped = False
        self.started = False

    def stop(self):
        """
        Stops all clips.
        """

        # stop all players that are attached
        for (n, p) in self.players.items():
            # this is needed if the players are set to infinite repeat
            # so they won't restart
            p.stopped = True
            # this removes the players
            p.stop()

        # clear the list of things that are playing, in case we start more
        self.clips = []
        self.players = {}
        self.stopped = True

    async def advance(self):

        """
        return all events from now to TIME_INTERVAL and then move the time index up by that amount.
        the multiplayer doesn't keep track of the time indexes themselves, the clips do, and they may
        all run at different speeds.
        """

        self.callbacks.on_multiplayer_advance()

        my_players = [ p for p in self.players.values() ]

        wait_times = [ t for t in [ p2.wait_time() for p2 in [ p for p in my_players if p.has_events() ]] if t > 0 ]

        now = time.perf_counter()

        if len(wait_times) == 0:
            wait_time = MILLISECONDS
        else:
            wait_time = min(wait_times) - MILLISECONDS
            if wait_time < MILLISECONDS:
                wait_time = MILLISECONDS

        for p in my_players:
            p.advance(wait_time, now)

        await zsleep(wait_time)

    def add_scene(self, scene):
        """
        Plays all clips in a scene, first stopping all clips that might be playing elsewhere.
        """

        self.stopped = False
        self.callbacks.on_scene_start(scene)
        clips = scene.clips(self.song)

        self.add_clips(clips)

    def add_clips(self, clips):
        """
        Adds a clip to be playing by creating a Player for it.
        """

        for clip in clips:

            # starts a clip playing, including stopping any already on the same track
            self.callbacks.on_clip_start(clip)

            clip.reset()

            need_to_stop = [ c for c in self.clips if clip.track.obj_id == c.track.obj_id ]
            for c in need_to_stop:
                self.remove_clip(c)

            matched = [ c for c in self.clips if c.name == clip.name ]
            if not len(matched):
                # if the clip does not already have a player, make one
                self.clips.append(clip)
                player = clip.get_player(self.song, self.engine_class)
                self.players[clip.name] = player
                player._multiplayer = self

        for (k,v) in self.players.items():
            v.start()

        self.started = True

    def remove_clips_with_track(self, track):

        remove_these = [ c for c in self.song.all_clips() if c.track == track ]
        for clip in remove_these:
            self.remove_clip(clip)


    def remove_clip(self, clip, add_pending=False):
        """
        Stops a clip and removes the player for it.
        """

        if not clip.name in self.players:
            return

        self.callbacks.on_clip_stop(clip)

        player = self.players[clip.name]
        player.stop()
        del self.players[clip.name]
        self.clips = [ c for c in self.clips if c.name != clip.name ]

        if not add_pending and len(self.clips) == 0 and self.stop_if_empty:
            self.stop()
