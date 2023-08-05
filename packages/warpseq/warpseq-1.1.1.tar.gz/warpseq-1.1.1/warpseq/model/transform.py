# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# a transform is a list of modifier expressions that can be used
# to build MIDI effects including Arps.

from ..utils.utils import roller
from .base import NewReferenceObject
from .directions import *
from warpseq.model.context import Context
from warpseq.model.slot import Slot
import sys
from warpseq.api.exceptions import WebSlotCompilerException
from warpseq.parser.web_slots import WebSlotCompiler

CHORDS = 'chords'
NOTES = 'notes'
BOTH = 'both'
APPLIES_CHOICES = [ CHORDS, NOTES, BOTH ]

class Transform(NewReferenceObject, Directionable):

    __slots__ = [ 'name', 'slots', 'arp', '_current_slots', 'divide', 'applies_to', 'obj_id',
                  'direction', '_current_direction', '_iterator', '_slot_mods', 'auto_reset', 'audition_instrument',
                  'audition_pattern', 'web_slots', '_played_ts']

    # ==================================================================================================================

    def __init__(self, name=None, slots=None, divide=None, obj_id=None,
                 applies_to=BOTH, direction=FORWARD, auto_reset=False, arp=True, audition_instrument=None,
                 audition_pattern=None, web_slots=None):

        if not slots and not web_slots:
            web_slots = [ dict() for x in range(0,5) ]

        self.slots = slots
        self.set_slots_from_web_slots(web_slots)

        # we'll add in web_slots compile soon
        if self.slots is None:
            self.slots = []

        self.name = name

        self.divide = divide
        self.applies_to = applies_to
        self.obj_id = obj_id
        self._slot_mods = roller(slots)
        self.direction = direction
        self._current_direction = direction
        self.auto_reset = auto_reset
        self.applies_to = applies_to
        self.audition_instrument = audition_instrument
        self.audition_pattern = audition_pattern
        self.arp = arp

        assert applies_to in APPLIES_CHOICES

        self._played_ts = None

        self.reset()

        super(Transform, self).__init__()

    # ==================================================================================================================

    def _get_should_process_and_arpeggiate(self, chord):
        # what should happen to this chord/note ?

        process = True
        arpeggiate = True

        if len(chord.notes) == 1:
            if self.applies_to not in [BOTH, NOTES]:
                process = False
                arpeggiate = False
        else:
            if self.applies_to not in [BOTH, CHORDS]:
                process = False
                arpeggiate = False

        return (process, arpeggiate)

    # ==================================================================================================================

    def _get_effective_divide(self, chord):
        # how many steps should we slice this into?

        if self.divide is not None:
            return self.divide
        return len(chord.notes)

    # ==================================================================================================================

    def _get_notes_iterator(self, chord, arpeggiate):
        # what should we play as we repeat this step?

        if not arpeggiate:
            return utils.forever(chord)
        return utils.roller(chord.notes)

    # ==================================================================================================================

    def process(self, song, pattern, scale, track, chord_list, t_start, slot_duration):

        results = []
        context = Context(song=song, pattern=pattern, scale=scale, track=track, base_length=slot_duration)

        if self.auto_reset:
            self.reset()

        for chord in chord_list:

            if chord is None:
                continue

            (process, arpeggiate) = self._get_should_process_and_arpeggiate(chord)
            divide = self._get_effective_divide(chord)

            if not self.arp:
                arpeggiate = False

            notes_iterator = self._get_notes_iterator(chord, arpeggiate)

            original_start = chord.notes[0].start_time
            original_end = chord.notes[0].end_time
            delta = original_end - original_start
            new_delta = delta / divide

            n_start = original_start
            n_end = original_start + new_delta

            for _ in range(0, divide):

                my_slot = self.get_next()

                this_note = next(notes_iterator)
                transformed = my_slot.evaluate(context, this_note)

                if transformed is None:
                    results.append([])
                    continue

                results.append(transformed.with_timing(
                    start_time = n_start,
                    end_time = n_end,
                    length = new_delta
                ))

                n_start = n_start + new_delta
                n_end = n_end + new_delta

        return results

    # ===================================================================================================================

    def set_slots_from_web_slots(self, web_slots):
         # TODO: lots of duplication with pattern.py in these, make a common base class

         """
         When deserializing web slots, run the compiler to generate the actual slot objects the engine can run on.
         """

         ok = True
         errors = None
         if web_slots is not None:
             (ok, slots, errors) =  WebSlotCompiler(for_transform=True, pattern_type=None).compile(web_slots)
             if not ok:
                 return
             else:
                 self.slots = slots
         else:
             if self.slots is None:
                 self.slots = []
         self.web_slots = web_slots
         if not ok:
             raise WebSlotCompilerException(errors)

    def get_web_slot_grid_for_ui(self, category):
        return WebSlotCompiler(for_transform=True, pattern_type=None).get_grid(self.web_slots, category)

    def update_web_slots_for_ui(self, data):
        new_web_slots = WebSlotCompiler(for_transform=True, pattern_type=None).update_web_slots_from_ui(self.web_slots, data)
        self.set_slots_from_web_slots(new_web_slots)

    def delete_web_slot_rows(self, data):
        # TODO: copied from pattern, reduce duplication
        new_web_slots = []
        for (i,x) in enumerate(self.web_slots):
            if i not in data:
                new_web_slots.append(x)
        self.set_slots_from_web_slots(new_web_slots)