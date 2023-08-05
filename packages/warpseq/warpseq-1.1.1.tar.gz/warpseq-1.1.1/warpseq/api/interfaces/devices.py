# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model import device
from warpseq.api.interfaces.base import CollectionApi
from warpseq.playback import midi

class Devices(CollectionApi):

    object_class    = device.Device
    public_fields   = [ 'name' ]
    song_collection = 'devices'
    add_method      = 'add_devices'
    add_required    = [ ]
    edit_required   = None
    remove_method   = 'remove_device'
    nullable_edits  = [ ]

    def __init__(self, public_api, song):
        super().__init__(public_api, song)
        self.auto_add_discovered()

    def list_available(self):
        """
        Return the names of all available MIDI devices the program can use.
        """
        return midi.get_devices()

    def add(self, name):
        if name not in self.list_available():
            raise MIDIConfigError("MIDI device named (%s) is not available on this computer" % name)
        return self._generic_add(name, locals())

    def auto_add_discovered(self):
        available = self.list_available()

        # add any devices from the computer config not in the present state
        for x in available:
            if not self.lookup(x):
                self.add(x)

        devices = [ x for x in self.song.devices.values() ]

        # remove devices that are not currently attached to the computer
        # this could happen if loading someone else's song file.
        for device in devices:
            if device.name not in available:
                for instrument in self.song.instruments.values():
                    if instrument.device == device:
                        instrument.device = None
                self.song.remove_device(device)

