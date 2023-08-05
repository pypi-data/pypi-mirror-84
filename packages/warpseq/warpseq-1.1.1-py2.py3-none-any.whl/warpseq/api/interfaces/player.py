# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.playback.realtime_engine import RealtimeEngine
from warpseq.playback.multi_player import MultiPlayer
from warpseq.api.exceptions import WarpException
from warpseq.model.clip import Clip
from warpseq.model.track import Track
from warpseq.model.scene import Scene
import sys
import traceback
import asyncio

TEMP_TRACK = "__TEMP_TRACK"
TEMP_SCENE = "__TEMP_SCENE"
TEMP_CLIP  = "__TEMP_CLIP"

class Player(object):

    def __init__(self, public_api, song):

        self.public_api = public_api
        self.song = song
        self.multi_player = MultiPlayer(song=song, engine_class=RealtimeEngine)

    def add_scene(self, scene):

        self.public_api.data_pools.reset_all()

        # TODO: this needs to learn how to wait until the next bar length.
        self.multi_player.stopped = False
        scene = self.public_api.scenes.lookup(scene, require=True)
        self.multi_player.add_scene(scene)

    def add_first_scene(self):

        self.public_api.data_pools.reset_all()

        self.multi_player.stopped = False
        list_scenes = self.song.scenes[:]
        if len(list_scenes) ==0:
            return
        self.multi_player.add_scene(list_scenes[0])

    def add_scene_id(self, scene):

        self.public_api.data_pools.reset_all()

        # TODO: this needs to learn how to wait until the next bar length.
        self.multi_player.stopped = False # TODO: this shouldn't be part of the API contract, eliminate
        scene = self.public_api.scenes.lookup(id=scene, require=True)
        self.multi_player.add_scene(scene)

    def add_clips(self, clips): # by name
        # TODO: this needs to learn how to wait until the next bar length.
        self.multi_player.stopped = False
        clips = [ self.public_api.clips.lookup(c, require=True) for c in clips ]
        self.multi_player.add_clips(clips)

    def add_clip_ids(self, clips): # by id
        # TODO: this needs to learn how to wait until the next bar length.
        self.multi_player.stopped = False
        clips = [ self.public_api.clips.lookup(id=c, require=True) for c in clips ]
        self.multi_player.add_clips(clips)

    def audition_pattern(self, pattern):
        # TODO: this is only surfaced for API testing, can remove
        pattern = self.public_api.patterns.lookup(name=pattern, require=True)
        print("LOOKED UP PATTERN TO AUDITION: %s" % pattern)
        self._audition_pattern_obj(pattern)

    def audition_pattern_id(self, pattern):
        pattern = self.public_api.patterns.lookup(id=pattern, require=True)
        self._audition_pattern_obj(pattern)

    def _audition_pattern_obj(self, pattern):
        temp_track = Track(name=TEMP_TRACK, instruments=[pattern.audition_with], hidden=True)
        temp_scene = Scene(name=TEMP_SCENE, hidden=True)
        temp_clip = Clip(name=TEMP_CLIP, obj_id=TEMP_CLIP, scene=temp_scene, track=temp_track, patterns=[pattern], repeat=None)
        print("ADDING TEMP CLIPS: %s" % temp_clip)
        self.multi_player.add_clips([temp_clip])

    def audition_transform(self, transform):
        # TODO: this is only surfaced for API testing, can remove
        transform = self.public_api.transforms.lookup(name=transform, require=True)
        self._audition_transform_obj(transform)

    def audition_transform_id(self, transform):
        transform = self.public_api.transforms.lookup(id=transform, require=True)
        self._audition_transform_obj(transform)

    def _audition_transform_obj(self, transform):
        self.public_api.data_pools.reset_all()

        pattern = transform.audition_pattern
        if not pattern:
            return
        temp_track = Track(name=TEMP_TRACK, instruments=[pattern.audition_with], hidden=True)
        temp_scene = Scene(name=TEMP_SCENE, hidden=True)
        temp_clip = Clip(name=TEMP_CLIP, obj_id=TEMP_CLIP, scene=temp_scene, track=temp_track, patterns=[pattern],
                         transforms=[transform], repeat=None)
        self.multi_player.add_clips([temp_clip])

    def _audition_clip_obj(self, clip):
        self.public_api.data_pools.reset_all()

        patterns = clip.patterns
        transforms = clip.transforms
        scales = clip.scales
        rate = clip.rate
        tempo_shifts = clip.tempo_shifts

        temp_track = clip.track #Track(name=TEMP_TRACK, instrument=pattern.audition_with, hidden=True)
        temp_scene = Scene(name=TEMP_SCENE, hidden=True)
        temp_clip = Clip(name=TEMP_CLIP, obj_id=TEMP_CLIP, scene=temp_scene, track=temp_track, patterns=patterns,
                         scales=scales, transforms=transforms, rate=rate, tempo_shifts=tempo_shifts, repeat=0, auto_scene_advance=False)
        self.multi_player.add_clips([temp_clip])

    def audition_clip_slot(self, clip_id, slot_number):
        clip = self.public_api.clips.lookup(id=clip_id, require=True)

        patterns = []
        transforms = []
        tempo_shifts = []
        scales = []

        if len(clip.patterns) > slot_number:
           patterns = [ clip.patterns[slot_number] ]

        if len(clip.transforms) > slot_number:
            transforms = clip.transforms[slot_number]
            if type(transforms) not in [ list, tuple ]:
                transforms = [ transforms ]

        if len(clip.scales) > slot_number:
            scales = [ clip.scales[slot_number] ]

        if len(clip.tempo_shifts) > slot_number:
            tempo_shifts = [ clip.tempo_shifts[slot_number] ]

        temp_track = clip.track
        temp_scene = Scene(name=TEMP_SCENE, hidden=True)
        temp_clip = Clip(name=TEMP_CLIP, obj_id=TEMP_CLIP, scene=temp_scene, track=temp_track, patterns=patterns,
                         scales=scales, transforms=transforms, rate=clip.rate, tempo_shifts=tempo_shifts, repeat=1, auto_scene_advance=False)
        self.multi_player.add_clips([temp_clip])

    def audition_clip_id(self, clip):
        clip = self.public_api.clips.lookup(id=clip, require=True)
        self._audition_clip_obj(clip)

    def stop_track_id(self, track):
        track = self.public_api.tracks.lookup(id=track, require=True)
        self.multi_player.remove_clips_with_track(track)

    def stop(self):
        self.multi_player.stop()

    async def advance(self):
        await self.multi_player.advance()

    def loop(self, scene=None, infinite=False):
        return asyncio.run(self._loop(scene=scene, infinite=infinite))

    async def _loop(self, scene=None, infinite=False):

        self.multi_player.stopped = False

        if scene:
            self.add_scene(scene)

        try:
            while True:

                await self.advance()
                if self.multi_player.stopped:
                    if not infinite:
                        return
                    else:
                        pass

        except KeyboardInterrupt:

            self.public_api._callbacks.keyboard_interrupt()
            self.stop()
            return

        except WarpException:
            traceback.print_exc()
            return



