# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.data_pool import DataPool
from warpseq.api.interfaces.base import CollectionApi

class DataPools(CollectionApi):

    object_class    = DataPool
    public_fields   = [ 'name', 'direction', 'length' ]
    song_collection = 'data_pools'
    add_method      = 'add_data_pools'
    add_required    = [ 'slots' ]
    edit_required   = [ ]
    remove_method   = 'remove_data_pool'
    nullable_edits  = [ ]

    def add(self, name, slots:list=None, direction='forward', length=None):
        params = locals()
        return self._generic_add(name, params)

    def edit(self, name:str=None, id:str=None, new_name:str=None, slots:list=None, direction=None, length=None, web_slots:dict=None):
        params = locals()

        obj = self.lookup(name=name, id=id, require=True)
        old_dir = obj.direction

        res = self._generic_edit(name, params)

        if direction != old_dir:
            obj.reset()

        return res

    def delete(self, id=None):
        # FIXME: this leaves any references in the pattern webslots ... and probably shouldn't.  Errors should be ignored though.
        obj = self.lookup(id=id, require=True)
        return self._generic_remove(obj.name)

    def get_web_slot_grid_for_ui(self, id: str = None):
        obj = self.lookup(id=id, require=True)
        return obj.get_web_slot_grid_for_ui()

    def update_web_slots_for_ui(self, id: str = None, data=None):
        obj = self.lookup(id=id, require=True)
        return obj.update_web_slots_for_ui(data)

    def delete_web_slot_rows(self, id:str=None, data=None):
        obj = self.lookup(id=id, require=True)
        return obj.delete_web_slot_rows(data)

    def reset_all(self):
        for pool in self.song.all_data_pools():
            pool.reset()