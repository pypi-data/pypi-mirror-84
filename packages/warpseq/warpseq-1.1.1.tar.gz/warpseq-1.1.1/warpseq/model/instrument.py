# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# an instrument adds a channel number to a MIDI device and has some
# parameters around supported note ranges. It can also be muted.

from .base import NewReferenceObject
import functools

class Instrument(NewReferenceObject):

    __slots__ = [ 'name', 'channel', 'device', 'min_octave', 'base_octave', 'max_octave', 'default_velocity', 'muted', '_played_ts',
                'drum1_note',
                'drum1_octave',
                'drum2_note',
                'drum2_octave',
                'drum3_note',
                'drum3_octave',
                'drum4_note',
                'drum4_octave',
                'drum5_note',
                'drum5_octave',
                'drum6_note',
                'drum6_octave',
                'drum7_note',
                'drum7_octave',
                'drum8_note',
                'drum8_octave',
                ]

    def __init__(self, name=None, channel=1, device=None, min_octave=0, base_octave=3, max_octave=10,
                 default_velocity=120, muted=False, obj_id=None,
                 drum1_note='C', drum1_octave=4,
                 drum2_note='D', drum2_octave=4,
                 drum3_note='E', drum3_octave=4,
                 drum4_note='F', drum4_octave=4,
                 drum5_note='G', drum5_octave=4,
                 drum6_note='C', drum6_octave=5,
                 drum7_note='D', drum7_octave=5,
                 drum8_note='E', drum8_octave=5,
                 ):

        self.name = name

        if channel is not None:
            channel = int(channel)

        self.channel = channel
        self.device = device
        self.min_octave = min_octave
        self.base_octave = base_octave
        self.max_octave = max_octave
        self.default_velocity = default_velocity
        self.muted = muted
        self.obj_id = obj_id

        self.drum1_note = drum1_note
        self.drum2_note = drum2_note
        self.drum3_note = drum3_note
        self.drum4_note = drum4_note
        self.drum5_note = drum5_note
        self.drum6_note = drum6_note
        self.drum7_note = drum7_note
        self.drum8_note = drum8_note

        self.drum1_octave = int(drum1_octave)
        self.drum2_octave = int(drum2_octave)
        self.drum3_octave = int(drum3_octave)
        self.drum4_octave = int(drum4_octave)
        self.drum5_octave = int(drum5_octave)
        self.drum6_octave = int(drum6_octave)
        self.drum7_octave = int(drum7_octave)
        self.drum8_octave = int(drum8_octave)

        self._played_ts = None

        super(Instrument,self).__init__()

    @functools.lru_cache()
    def get_midi_out(self):
        return self.device.get_midi_out()
