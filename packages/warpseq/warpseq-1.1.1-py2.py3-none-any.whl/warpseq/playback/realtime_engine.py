# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# this class is used by the player code to send MIDI events to hardware
# it contains some logic to convert chords to note events and must also
# process deferred mod-expressions caused by late-binding intra-track
# events.

from warpseq.api.callbacks import Callbacks
# from warpseq.api.exceptions import *
from warpseq.model.registers import register_playing_note, unregister_playing_note
from warpseq.model.chord import Chord
from warpseq.model.event import NOTE_OFF, NOTE_ON
from warpseq.model.pattern import PERCUSSION

# ======================================================================================================================

def _get_note_number(note, instrument, pattern):

    max_o = instrument.max_octave
    min_o = instrument.min_octave

    if pattern.pattern_type == PERCUSSION:
        note2 = note.copy()
    else:
        note2 = note.copy().transpose(octaves=instrument.base_octave)

    # wrap the note to the valid octave range
    if note2.octave > max_o:
        note2.octave = max_o
    if note2.octave < min_o:
        note2.octave = min_o

    nn = note2.note_number()

    # this shouldn't happen anymore because of the above octave wrap
    if nn < 0 or nn > 127:
        print("warning: note outside of playable range: %s" % note2)
        return None

    return nn

# ======================================================================================================================

class RealtimeEngine(object):

    __slots__ = ['midi_out','midi_port','callbacks']

    # ------------------------------------------------------------------------------------------------------------------


    def __init__(self):

        self.callbacks = Callbacks()

    # ------------------------------------------------------------------------------------------------------------------

    def _process_deferred(self, evt):

        # deferred expressions are mostly track grab events, which have to be evaluated right before
        # the notes need to play

        exprs = evt.note.deferred_expressions
        for expr in exprs:
            value = expr.evaluate(evt.track, evt.note)
            if value is None:
                evt.note = None
                return
            evt.note = value

    # ------------------------------------------------------------------------------------------------------------------

    def _play_notes(self, event, now):

        mode = event.track.instrument_mode

        # various logic dealing with hocketing and so on, we might use the same instrument for all notes,
        # we might not.

        chosen = event.track.before_instrument_select(mode)

        for (i, x) in enumerate(event.note.notes):

            if x.muted:
                return

            evt = event.copy()
            evt.note = x

            # actual logic of deciding what instrument to play
            evt.instruments = event.track.get_instruments(evt, chosen, mode)

            self._process_deferred(evt)

            if evt.note is None:
                # ignore rests
                return

            self.play(evt, now)

    # ------------------------------------------------------------------------------------------------------------------

    def _play_note_on(self, event, now):

        # this makes the status lights function
        event.mark_playing(now)

        pattern = event.from_context.pattern

        # this makes track grabs be able to pick up notes
        register_playing_note(event.track, event.note)

        # process MIDI CC requests
        for (control, value) in event.note.ccs.items():
            control = int(control)
            for instrument in event.get_instruments():
                instrument.device.midi_cc(instrument.channel, control, int(value))

        if not (event.track.muted or event.note.muted):

            # this is also related to status lights
            event.track._played_ts = now

            # record when the off version of this on event should play
            event.player.inject_off_event(event)

            # fire the MIDI signal for every device/channel combination

            for instrument in event.get_instruments():

                instrument._played_ts = now
                if instrument.device:
                    instrument.device._played_ts = now

                velocity = event.note.velocity
                if velocity is None:
                    velocity = instrument.default_velocity

                if not instrument.muted and instrument.device:
                    # TODO: this should probably be a callback
                    #print("PLAY ON %s:" % (event.note))
                    instrument.device.midi_note_on(instrument.channel,
                                 _get_note_number(event.note, instrument, pattern), velocity)

    # ------------------------------------------------------------------------------------------------------------------

    def _play_note_off(self, event, now):

        pattern = event.from_context.pattern
        unregister_playing_note(event.track, event.on_event.note)

        for instrument in event.get_instruments():

            velocity = event.note.velocity
            if velocity is None:
                velocity = instrument.default_velocity

            if not instrument.muted and instrument.device:
                # TODO: this should probably be a callback
                #print("PLAY OFF: %s" % (event.note))
                instrument.device.midi_note_off(instrument.channel,
                              _get_note_number(event.note, instrument, pattern), velocity)

    # ------------------------------------------------------------------------------------------------------------------

    def play(self, event, now):
        """
        Fire off an MIDI on or off event.  Now is the current time for use in setting status light information.
        """

        if not event.note:
            return
        if type(event.note) == Chord:
            self._play_notes(event, now)
            return
        if event.type == NOTE_ON:
            self._play_note_on(event, now)
        elif event.type == NOTE_OFF:
            self._play_note_off(event, now)
        else:
            raise Exception("unknown event type")


