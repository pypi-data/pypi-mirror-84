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
from warpseq.model.slot import Slot
from warpseq.parser.web_slots import WebSlotCompiler

STANDARD = 'standard'
PERCUSSION = 'percussion'
PATTERN_TYPES = [ STANDARD, PERCUSSION ]

class Pattern(NewReferenceObject, Directionable):

    __slots__ = [ 'name', 'slots', '_current_slots', 'octave_shift', 'rate', 'scale', 'direction', '_current_direction',
                  'length', '_iterator', 'obj_id', 'audition_with', 'web_slots', 'pattern_type', 'drum_config', '_played_ts' ]

    def __init__(self, name=None, slots=None, octave_shift=0, rate=1, scale=None, direction=FORWARD, length=None,
                 obj_id=None, audition_with=None, web_slots=None, pattern_type=STANDARD, drum_config=None):

        self.obj_id = obj_id

        # length is not surfaced in the UI presently, and if set, only the first N notes of the pattern are used.
        self.length = length

        self.pattern_type = pattern_type

        if not slots and not web_slots:
            # default the web UI view to 8 slots in the pattern grid
            web_slots = [ dict() for _ in range(0,8) ]

        self.drum_config = drum_config
        self.name = name
        self.slots = slots
        self.direction = direction
        self._current_direction = direction

        self.set_slots_from_web_slots(web_slots)
        self.web_slots = web_slots

        self.octave_shift = octave_shift
        self.rate = rate
        self.scale = scale
        self.audition_with = audition_with

        if not self.slots:
            self.slots = []

        for x in self.slots:
            assert isinstance(x, Slot)

        if length is None:
            length = len(self.slots)

        self.length = length

        if not direction in DIRECTIONS:
            raise InvalidInput("direction must be one of: %s" % DIRECTIONS)

        self._played_ts = None

        super(Pattern, self).__init__()
        self.reset()

    def set_slots_from_web_slots(self, web_slots):

        """
        When deserializing web slots, run the compiler to generate the actual slot objects the engine can run on.
        """

        old_length = self.length

        ok = True
        errors = None
        if web_slots is not None:
            (ok, slots, errors) =  WebSlotCompiler(for_transform=False, pattern_type=self.pattern_type).compile(web_slots)
            if not ok:
                # do not update the slots, leave them as is
                return
            else:
                self.slots = slots
        else:
            if self.slots is None:
                self.slots = []
        self.web_slots = web_slots
        self.length = len(self.slots)

        # TODO: we need to do this in transforms and data pools too - already done or not?
        if self.length != old_length:
            self.reset()

        if not ok:
            raise WebSlotCompilerException(errors)

    def get_web_slot_grid_for_ui(self, category):
        return WebSlotCompiler(for_transform=False, pattern_type=self.pattern_type).get_grid(self.web_slots, category)

    def update_web_slots_for_ui(self, data):
        new_web_slots = WebSlotCompiler(for_transform=False, pattern_type=self.pattern_type).update_web_slots_from_ui(self.web_slots, data)
        self.set_slots_from_web_slots(new_web_slots)

    def delete_web_slot_rows(self, data):
        new_web_slots = []
        for (i,x) in enumerate(self.web_slots):
            if i not in data:
                new_web_slots.append(x)
        self.set_slots_from_web_slots(new_web_slots)

    def get_octave_shift(self, track):
        return self.octave_shift

    def get_length(self):
        return self.length

    def get_iterator(self):

        if not self.slots:
            return None

        for _ in range(0, self.get_length()):
            if self.length_mismatch():
                self.reset()
            index = next(self._iterator)

            res = self.slots[index]
            yield res
