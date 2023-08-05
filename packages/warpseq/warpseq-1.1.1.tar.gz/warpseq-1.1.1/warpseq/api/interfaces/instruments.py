# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.instrument import Instrument
from warpseq.api.interfaces.base import CollectionApi

class Instruments(CollectionApi):

    object_class    = Instrument
    public_fields   = [ 'name', 'channel', 'device', 'muted', 'min_octave', 'max_octave', 'base_octave', 'default_velocity',
                        'drum1_note', 'drum1_octave', 'drum2_note', 'drum2_octave', 'drum3_note', 'drum3_octave',
                        'drum4_note',  'drum4_octave', 'drum5_note', 'drum5_octave', 'drum6_note', 'drum6_octave',
                        'drum7_note', 'drum7_octave', 'drum8_note', 'drum8_octave',
                        ]
    song_collection = 'instruments'
    add_method      = 'add_instruments'
    add_required    = [ 'channel', 'device']
    edit_required   = [ ]
    remove_method   = 'remove_instrument'
    nullable_edits  = [ ]

    def add(self, name, channel:int=1, device:str=None, min_octave:int=0, max_octave:int=10, base_octave:int=3, muted:bool=False, default_velocity:int=120):
        device = self.api.devices.lookup(device, require=True)
        return self._generic_add(name, locals())

    def edit(self, name=None, id:str=None, new_name:str=None, channel:int=None, device:str=None, min_octave:int=None, max_octave:int=None, base_octave:int=None, muted:bool=None, default_velocity:int=0,
             drum1_note=None, drum1_octave=3,
             drum2_note=None, drum2_octave=3,
             drum3_note=None, drum3_octave=3,
             drum4_note=None, drum4_octave=3,
             drum5_note=None, drum5_octave=3,
             drum6_note=None, drum6_octave=4,
             drum7_note=None, drum7_octave=4,
             drum8_note=None, drum8_octave=4,
             ):

        # because type hints are not useful, apparently
        if min_octave is not None:
            min_octave = int(min_octave)
        if max_octave is not None:
            max_octave = int(max_octave)
        if base_octave is not None:
            base_octave = int(base_octave)
        else:
            base_octave = 0
        if channel is not None:
            channel = int(channel)

        device = self.api.devices.lookup(device, require=True)
        return self._generic_edit(name, locals())

    def delete(self, id=None):
        obj = self.lookup(id=id, require=True)

        for track in self.song.tracks:
            if track.instruments:
                track.instruments = [ x for x in track.instruments if x != obj ]

        for pattern in self.song.all_patterns():
            if pattern.audition_with == obj:
                pattern.audition_with = None
            if pattern.drum_config == obj:
                pattern.drum_config = None

        return self._generic_remove(obj.name)

