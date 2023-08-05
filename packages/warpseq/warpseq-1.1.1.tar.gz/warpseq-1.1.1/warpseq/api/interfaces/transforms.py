# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.transform import Transform
from warpseq.api.interfaces.base import CollectionApi

class Transforms(CollectionApi):

    object_class     = Transform
    public_fields    = [ 'name', 'divide', 'applies_to', 'direction', 'auto_reset', 'arp', 'audition_instrument', 'audition_pattern' ]
    song_collection  = 'transforms'
    add_method       = 'add_transforms'
    add_required     = [ 'slots' ]
    edit_required    = [ ]
    remove_method    = 'remove_transform'
    nullable_edits   = [ ]

    def add(self, name, slots:list=None, divide:int=None, applies_to:str='both', direction='forward', arp=True, auto_reset=False, audition_instrument=None, audition_pattern=None):

        # TODO: remove duplication w/ methods below
        if audition_instrument:
            audition_instrument = self.api.instruments.lookup(audition_instrument, require=True)
        if audition_pattern:
            audition_pattern = self.api.patterns.lookup(audition_pattern, require=True)
        params = locals()

        return self._generic_add(name, params)

    def edit(self, name:str=None, id:str=None, new_name:str=None, slots:list=None, divide:int=None, applies_to:str=None, arp:bool=None,
             direction=None, auto_reset=None, audition_instrument=None, audition_pattern=None, web_slots:dict=None):

        if audition_instrument:
            audition_instrument = self.api.instruments.lookup(audition_instrument, require=True)
        if audition_pattern:
            audition_pattern = self.api.patterns.lookup(audition_pattern, require=True)

        if divide == "auto":
            divide = None
        if divide is not None:
            try:
                divide = int(divide)
            except:
                divide = 1

        params = locals()

        obj = self.lookup(name=name, id=id, require=True)
        old_dir = obj.direction



        res = self._generic_edit(name, params)

        if direction != old_dir:
            obj.reset()

        return res


    def delete(self, id=None):

        obj = self.lookup(id=id, require=True)
        assert obj is not None

        # ideally we want a "stop clip id" method on api.player
        self.api.player.stop()

        # patterns can be used in any clip, so we have to trim them
        # if we find them playing in any clips we must also stop those

        for clip in self.song.all_clips():

            if clip.has_transform(obj):

                clip.remove_transform(obj)

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