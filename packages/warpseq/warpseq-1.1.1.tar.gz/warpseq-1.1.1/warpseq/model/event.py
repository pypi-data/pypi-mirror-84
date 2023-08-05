# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# an event represents starting or stopping a note, and some associated
# data so the program can handle the note and other processing in context.
# for instance the scale is needed for processing deferred events.

from warpseq.model.chord import Chord

NOTE_ON = 1
NOTE_OFF = 0

class Event(object):

    __slots__ = [ 'type', 'note', 'time', 'on_event', 'from_context', 'instruments', 'song', 'track', 'clip', 'player' ]

    def __init__(self, type=None, note=None, time=None, on_event=None, from_context=None, instruments=None,
                 song=None, track=None, clip=None, player=None):

        self.type = type
        self.note = note
        self.time = time

        self.on_event = on_event

        self.from_context = from_context

        if instruments is None:
            instruments = []

        self.instruments = instruments

        self.song = song
        self.track = track
        self.clip = clip
        self.player = player

    def __repr__(self):
        return "Event<Note=%s, type=%s, time=%s, instruments=%s>" % (self.note, self.type, self.time, self.instruments)

    def get_instruments(self):
        if self.on_event:
            return [ x for x in self.on_event.instruments if x is not None ]
        return [ x for x in self.instruments if x is not None ]

    def copy(self):
        return Event(
            type = self.type,
            note = self.note.copy(), # could be a Chord!  Be careful.
            time = self.time,
            on_event = self.on_event,
            instruments = self.instruments,
            song = self.song,
            track = self.track,
            clip = self.clip,
            player = self.player,
            from_context = self.from_context
        )

    def mark_playing(self, ts):

        self.from_context.mark_playing(ts)

        # this should likely only be called on chord events only... but we'll do this on both anyway

        if type(self.note) == Chord:
            for x in self.note.notes:
                for t in x.recorded_transforms:
                    t._playing_ts = ts
        else:
            for t in self.note._transforms_recorded:
                t._played_ts = ts
