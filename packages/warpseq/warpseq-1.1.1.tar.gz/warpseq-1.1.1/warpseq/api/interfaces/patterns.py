# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.pattern import Pattern
from warpseq.api.interfaces.base import CollectionApi
from warpseq.api.exceptions import NotFound
import traceback
from warpseq.utils.cast import safe_int, safe_float


INTERNAL_AUDITION_SCENE = "!!INTERNAL/AUDITION_SCENE"
INTERNAL_AUDITION_TRACK = "!!INTERNAL/AUDITION_TRACK"
INTERNAL_AUDITION_CLIP  = "!!INTERNAL/AUDITION_CLIP"

class Patterns(CollectionApi):

    object_class    = Pattern
    public_fields   = [ 'name', 'octave_shift', 'scale', 'rate', 'direction', 'length', 'audition_with', 'pattern_type', 'drum_config']
    song_collection = 'patterns'
    add_method      = 'add_patterns'
    add_required    = [ 'slots' ]
    edit_required   = [ ]
    remove_method   = 'remove_pattern'
    nullable_edits   = [ 'scale' ]

    # ------------------------------------------------------------------------------------------------------------------

    def add(self, name, slots:list=None, scale=None, octave_shift=None, rate=1, direction='forward',
            audition_with=None, length=None):

        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        if audition_with:
            audition_with = self.api.instruments.lookup(audition_with, require=True)
        params = locals()
        return self._generic_add(name, params)

    # ------------------------------------------------------------------------------------------------------------------

    def edit(self, name:str=None, id:str=None, new_name:str=None, slots:list=None, scale:str=None, octave_shift:int=None,
             rate:int=None,  direction:str=None, audition_with:str=None, web_slots:dict=None, pattern_type:str=None, drum_config:str=None):

        if scale:
            scale = self.api.scales.lookup(scale, require=True)

        if audition_with:
            audition_with = self.api.instruments.lookup(audition_with, require=True)

        if drum_config:
            drum_config = self.api.instruments.lookup(drum_config, require=True)


        rate = safe_float(rate, 1)
        octave_shift = safe_int(octave_shift, 0)

        params = locals()

        obj = self.lookup(name=name, id=id, require=True)
        old_dir = obj.direction

        result = self._generic_edit(name, params)

        if direction != old_dir:
            obj.reset()

        return result

    # ------------------------------------------------------------------------------------------------------------------

    def delete(self, id=None):

        obj = self.lookup(id=id, require=True)

        # patterns can be used in any clip, so we have to trim them
        # if we find them playing in any clips we must also stop those

        self.api.player.stop()

        for clip in self.song.all_clips():

            if clip.has_pattern(obj):
                # TODO: call a method on player to stop just these clips.
                clip.remove_pattern(obj)

        return self._generic_remove(obj.name)

    # ------------------------------------------------------------------------------------------------------------------

    def get_web_slot_grid_for_ui(self, id:str=None, category:str=None):

        obj = self.lookup(id=id, require=True)
        return obj.get_web_slot_grid_for_ui(category)

    def update_web_slots_for_ui(self, id:str=None, data=None):
        obj = self.lookup(id=id, require=True)
        return obj.update_web_slots_for_ui(data)

    def delete_web_slot_rows(self, id:str=None, data=None):
        obj = self.lookup(id=id, require=True)
        return obj.delete_web_slot_rows(data)

