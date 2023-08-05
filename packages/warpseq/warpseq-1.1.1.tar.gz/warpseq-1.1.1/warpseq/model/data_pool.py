# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# a Pattern is a list of symbols/expressions that will eventually
# evaluate into Chords/Notes.

from .base import NewReferenceObject
from warpseq.api.exceptions import *
from warpseq.model.directions import *
from warpseq.model.slot import Slot, DataSlot
from warpseq.parser.data_slots import DataSlotCompiler

class DataPool(NewReferenceObject, Directionable):

    __slots__ = [ 'name', 'slots', '_current_slots', 'direction', '_current_direction', 'length',
                  '_iterator', 'obj_id', 'web_slots', '_played_ts' ]

    def __init__(self, name=None, slots=None, direction=FORWARD, length=None, obj_id=None, web_slots=None):

        if not slots and not web_slots:
            web_slots = [dict(value=1), dict(value=2), dict(value=3), dict(value=4)]

        self.slots = slots

        self.set_slots_from_web_slots(web_slots)

        if not self.slots:
            self.slots = []

        self.name = name

        for x in self.slots:
            assert isinstance(x, DataSlot)

        if not direction in DIRECTIONS:
            raise InvalidInput("direction must be one of: %s" % DIRECTIONS)

        self.direction = direction
        self._current_direction = direction
        self.obj_id = obj_id

        if length is None:
            length = len(self.slots)
        self.length = length

        self._played_ts = None
        super(DataPool, self).__init__()
        self.reset()

    def set_slots_from_web_slots(self, web_slots):

        # TODO: some but not total similarity with Pattern and Transform, refactor?

        ok = True
        errors = None
        if web_slots is not None:
            (ok, slots, errors) =  DataSlotCompiler().compile(web_slots)
            if not ok:
                # do not update the slots, leave them as is
                return
            else:
                self.slots = slots

        else:
            if self.slots is None:
                self.slots = []
        self.web_slots = web_slots
        self.length = len(self.web_slots)
        if not ok:
            raise WebSlotCompilerException(errors)

    def get_web_slot_grid_for_ui(self):
        return DataSlotCompiler().get_grid(self.web_slots)

    def update_web_slots_for_ui(self, data):
        new_web_slots = DataSlotCompiler().update_web_slots_from_ui(self.web_slots, data)
        self.set_slots_from_web_slots(new_web_slots)

    def delete_web_slot_rows(self, data):
        # TODO: copied from pattern, consolidate?

        new_web_slots = []
        for (i,x) in enumerate(self.web_slots):
            if i not in data:
                new_web_slots.append(x)
        self.set_slots_from_web_slots(new_web_slots)
