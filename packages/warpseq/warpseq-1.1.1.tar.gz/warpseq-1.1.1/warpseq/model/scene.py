# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# a scene is a set of clips that usually play together at the same time.

from .base import NewReferenceObject
from warpseq.model.clip import Clip

class Scene(NewReferenceObject):

    __slots__ = ('name', 'scale', 'auto_advance', 'rate', 'clip_ids', 'obj_id', 'hidden', '_played_ts' )

    SAVE_AS_REFERENCES = [ 'scale', ]

    def __init__(self, name=None, scale=None, auto_advance=True, rate=1, clip_ids=None, obj_id=None, hidden=False):

        self.name = name
        self.scale = scale
        self.auto_advance = auto_advance
        self.rate = rate
        self.clip_ids = clip_ids
        self.obj_id = obj_id
        self._played_ts = 0
        self.hidden = hidden

        if self.clip_ids is None:
            self.clip_ids = []

        super(Scene, self).__init__()

    def clips(self, song):
        results = [ song.find_clip(x) for x in self.clip_ids ]
        results = [ r for r in results if r is not None ]
        return results

    def add_clip(self, clip):
        if clip.obj_id not in self.clip_ids:
            self.clip_ids.append(clip.obj_id)

    def has_clip(self, clip):
        return clip.obj_id in self.clip_ids

    def remove_clip(self, clip):
        self.clip_ids = [ c for c in self.clip_ids if c != clip.obj_id ]

    def is_hidden(self):
        return self.hidden

    def _additional_web_copy_steps(self, song, from_obj):

        # prevent removing the clip from the previous track
        self.clip_ids = []

        from_clips = from_obj.clips(song)

        for clip in from_clips:

            track = clip.track
            obj_id = clip.new_object_id()

            clip_data = clip.to_dict()

            # TODO: this move through the serializer is a bit odd, at least we should have a copy
            # method that does it generically for all object types

            new_clip = Clip.from_dict(song, clip_data)
            new_clip.scene = None
            new_clip.track = None
            new_clip.name = '%s___%s' % (clip.name, obj_id)
            new_clip.obj_id = obj_id

            song.add_clip(scene=self, track=track, clip=new_clip)

