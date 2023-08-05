# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# the song is the fundamental unit of saving/loading in Warp and contains
# all object types.

import json

from warpseq.model.base import NewReferenceObject
from warpseq.model.status import status_report

FORMAT_VERSION = 0.1
DEFAULT_NAME = 'Warp Song'

TRACK_HEADER_TEMPLATE = """
<div class="ag-cell-label-container" role="presentation">
<span ref="eMenu" class="ag-header-icon ag-header-cell-menu-button"></span>
<div ref="eLabel" class="ag-header-cell-label" role="presentation">
<span ref="eSortOrder" class="ag-header-icon ag-sort-order" ></span>
<span ref="eSortAsc" class="ag-header-icon ag-sort-ascending-icon" ></span>
<span ref="eSortDesc" class="ag-header-icon ag-sort-descending-icon" ></span>
<span ref="eSortNone" class="ag-header-icon ag-sort-none-icon" ></span>
<a href="#" onclick="load_into_nav(TRACK);load_track_item('%s')"> <span ref="eText" class="ag-header-cell-text" role="columnheader"></span></a>
<span ref="eFilter" class="ag-header-icon ag-filter-icon"></span>
</div>
</div>
"""

SAVE_FIRST = [ 'devices', 'instruments', 'scales', 'data_pools', 'patterns', 'transforms', 'scenes', 'tracks', 'clips' ]

class Song(NewReferenceObject):

    __slots__ = [ 'name',  'devices', 'instruments', 'tracks', 'clips', 'scale', 'tempo',  'scales', 'scenes',
                  'transforms', 'patterns', 'data_pools', 'obj_id', 'filename', '_SAVE_FIRST' ]

    def __init__(self, name='Warp Song', clips = None, scale=None, tempo=120, devices=None, instruments=None, scales=None,
                 scenes=None, tracks=None, transforms=None, patterns=None, data_pools=None, obj_id=None, filename='warp.json'):

        self.name = name
        self.clips = clips
        self.scale = scale
        self.tempo = tempo
        self.devices = devices
        self.instruments = instruments
        self.scales = scales
        self.scenes = scenes
        self.tracks = tracks
        self.transforms = transforms
        self.patterns = patterns
        self.data_pools = data_pools
        self.obj_id = obj_id
        self.filename = filename

        self._SAVE_FIRST = SAVE_FIRST

        super(Song, self).__init__()

        self.reset(clear=False)

    def status_report(self):
        return status_report(self)

    def details(self):
        # return public fields - this is a bit different from other classes as this is the top level object
        results =  dict(
            name = self.name,
            tempo = self.tempo,
            filename = self.filename,
        )
        if self.scale:
            results['scale'] = self.scale.name
        else:
            results['scale'] = None
        return results

    def reset(self, clear=True):
        if clear or self.devices is None:
            self.devices = dict()
        if clear or self.instruments is None:
            self.instruments = dict()
        if clear or self.scales is None:
            self.scales = dict()
        if clear or self.tracks is None:
            self.tracks = []
        if clear or self.scenes is None:
            self.scenes = []
        if clear or self.clips is None:
            self.clips = dict()
        if clear or self.transforms is None:
            self.transforms = dict()
        if clear or self.patterns is None:
            self.patterns = dict()
        if clear or self.data_pools is None:
            self.data_pools = dict()
        if clear:
            self.filename = ""

    def find_device(self, obj_id):
        """
        Returns the device with the given object ID.
        This method and others like this are used for save/load support.
        """
        return self.devices.get(obj_id, None)

    def find_instrument(self, obj_id):
        """
        Returns the instrument with the given object ID.
        """
        return self.instruments.get(str(obj_id), None)

    def find_scale(self, obj_id):
        """
        Returns the scale with the given object ID.
        """
        return self.scales.get(str(obj_id), None)

    def find_scene(self, obj_id):
        """
        Returns the scene with the given object ID.
        """
        matching = [ x for x in self.scenes if str(x.obj_id) == str(obj_id) ]
        if len(matching) == 0:
            return None
        return matching[0]

    def find_track(self, obj_id):
        """
        Returns the track with the given object ID.
        """
        matching = [ x for x in self.tracks if str(x.obj_id) == str(obj_id) ]
        if len(matching) == 0:
            return None

        return matching[0]

    def find_clip(self, obj_id):
        """
        Returns the clip with the given object ID.
        """
        return self.clips.get(str(obj_id), None)

    def find_clip_by_name(self, name):
        """
        Returns the clip with the given name.
        """
        for (k,v) in self.clips.items():
            if v.name == name:
                return v
        return None

    def find_track_by_name(self, name):
        for v in self.tracks:
            if v.name == name:
                return v
        return None

    def find_transform(self, obj_id):
        """
        Returns the transform with the given object ID.
        """
        x = self.transforms.get(str(obj_id), None)
        return x

    def find_pattern(self, obj_id):
        """
        Returns the pattern with the given object ID.
        """
        return self.patterns.get(str(obj_id), None)

    def find_data_pool(self, obj_id):
        return self.data_pools.get(str(obj_id), None)

    def find_pattern_by_name(self, name):
        for (k,v) in self.patterns.items():
            if v.name == name:
                return v
        return None

    def find_scale_by_name(self, name):
        for (k,v) in self.scales.items():
            if v.name == name:
                return v
        return None

    def find_transform_by_name(self, name):
        for (k,v) in self.transforms.items():
            if v.name == name:
                return v
        return None

    def find_data_pool_by_name(self, name):
        for (k,v) in self.data_pools.items():
            if v.name == name:
                return v
        return None

    def to_dict(self):
        """
        Returns the data for the entire song file. This can be reversed with from_dict.
        """
        global FORMAT_VERSION
        data = super().to_dict()
        data['FORMAT_VERSION'] = FORMAT_VERSION
        data['OBJ_COUNTER'] = NewReferenceObject.new_object_id()
        return data

    def to_json(self):
        """
        Returns a saveable JSON version of the song file.
        """
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    @classmethod
    def from_dict(cls, data):

        # TODO: we should be able to use the deserializer here also? If not, explain why.

        """
        Loads a song from a dictionary.
        This must support PAST but not FUTURE versions of the program.
        """

        song = Song(name=data['name'])

        from . base import COUNTER

        format_version = data.get('FORMAT_VERSION', 0)
        if format_version > FORMAT_VERSION:
            # TODO: raise exception here?
            print("warning: likely cannot open data from a newer version of this program")

        COUNTER = data['OBJ_COUNTER']

        song.obj_id = data['obj_id']

        from . device import Device
        from . instrument import Instrument
        from . scale import Scale
        from . scene import Scene
        from . track import Track
        from . clip import Clip
        from . transform import Transform
        from . pattern import Pattern
        from . data_pool import DataPool

        song.scales = { str(k) : Scale.from_dict(song, v) for (k,v) in data['scales'].items() }
        # BOOKMARK
        song.devices = { str(k) : Device.from_dict(song, v) for (k,v) in data['devices'].items() }
        song.instruments =  { str(k) : Instrument.from_dict(song, v) for (k,v) in data['instruments'].items() }

        song.scenes = [ Scene.from_dict(song, v) for v in data['scenes'] ]
        song.tracks = [ Track.from_dict(song, v) for v in data['tracks'] ]

        song.transforms =  {str(k) : Transform.from_dict(song, v) for (k, v) in data['transforms'].items()}
        song.patterns =  { str(k) : Pattern.from_dict(song, v) for (k,v) in data['patterns'].items() }
        song.data_pools =  { str(k) : DataPool.from_dict(song, v) for (k,v) in data['data_pools'].items() }

        song.clips =  { str(k) : Clip.from_dict(song, v) for (k,v) in data['clips'].items() }

        song.scale = song.find_scale(data['scale'])
        song.tempo = data['tempo']

        return song

    def load_from_dict(self, data):

        loaded = Song.from_dict(data)

        self.name = loaded.name
        self.filename = loaded.filename
        self.tempo = loaded.tempo

        self.scales = loaded.scales
        self.devices = loaded.devices
        self.instruments = loaded.instruments
        self.scenes = loaded.scenes
        self.tracks = loaded.tracks

        self.transforms = loaded.transforms
        self.patterns = loaded.patterns
        self.data_pools = loaded.data_pools

        self.clips = loaded.clips
        self.scale = loaded.scale
        self.tempo = loaded.tempo
        self.obj_id = loaded.obj_id

    def all_clips(self):
        return [ x for x in self.clips.values() ]

    def all_patterns(self):
        return [ x for x in self.patterns.values() ]

    def all_data_pools(self):
        return [ x for x in self.data_pools.values() ]

    def next_scene(self, scene):
        """
        Returns the scene that is positioned after this one in the song.
        """
        index = None
        for (i,x) in enumerate(self.scenes):
            if x.obj_id == scene.obj_id:
                index = i
                break
        index = index + 1
        if index >= len(self.scenes):
            return None
        return self.scenes[index]

    @classmethod
    def from_json(cls, data):
        """
        Loads the song from JSON data, such as from a save file.
        """
        data = json.loads(data)
        return Song.from_dict(data)

    def _get_clip_index(self, scene=None, track=None):
        """
        Internal storage of clip uses a dict where the key is the combination of
        the scene and track object IDs.
        """
        index = "%s/%s" % (scene.obj_id, track.obj_id)
        return index

    def add_clip(self, scene=None, track=None, clip=None):
        """
        Adds a clip at the intersection of a scene and track.
        """

        # calling code must *COPY* the clip before assigning, because a clip must be added
        # to the clip list and *ALSO* knows its scene and track.

        previous = self.get_clip_for_scene_and_track(scene=scene, track=track)
        if previous and clip.obj_id == previous.obj_id:
            return

        if previous:
            self.remove_clip(scene=scene, track=track)

        self.clips[str(clip.obj_id)] = clip

        clip.track = track
        clip.scene = scene

        track.add_clip(clip)
        scene.add_clip(clip)

        return clip

    def remove_clip(self, scene=None, track=None, clip=None):
        """
        Deletes a clip.  The name isn't used - specify the scene and track.
        """

        # removing a clip returns a clip object that can be used with *assign* to add the
        # clip back.

        if not clip:
            clip = self.get_clip_for_scene_and_track(scene=scene, track=track)

        if clip is None:
            return None

        if not track:
            track = clip.track
        if not scene:
            scene = clip.scene

        track.remove_clip(clip)
        scene.remove_clip(clip)

        clip.track = None
        clip.scene = None

        del self.clips[clip.obj_id]

        return clip

    def get_clips_for_scene(self, scene=None):
        """
        Returns all clips in a given scene.
        """
        return scene.clips()

    def get_clip_for_scene_and_track(self, scene=None, track=None):
        """
        Returns the clip at the intersection of the scene and track.
        """
        results = []
        clips = scene.clips(self)
        for clip in clips:
            if track.has_clip(clip):
                results.append(clip)
        return self.one(results)

    def add_devices(self, devices):
        """
        Adds some device objects to the song.
        """
        for x in devices:
            self.devices[str(x.obj_id)] = x

    def remove_device(self, device):
        """
        Removes a device from the song.
        """
        del self.devices[str(device.obj_id)]

    def add_instruments(self, instruments):
        """
        Adds some instrument objects to the song
        """
        for x in instruments:
            self.instruments[str(x.obj_id)] = x

    def remove_instrument(self, instrument):
        """
        Removes an instrument object from the song.
        """
        del self.instruments[str(instrument.obj_id)]

    def add_scales(self, scales):
        """
        Adds some scale objects to a song.
        """
        for x in scales:
            self.scales[str(x.obj_id)] = x

    def remove_scale(self, scale):
        """
        Removes a scale object from the song.
        """
        del self.scales[str(scale.obj_id)]

    def add_tracks(self, tracks):
        """
        Adds some track objects to the song.
        """
        self.tracks.extend(tracks)

    def remove_track(self, track):
        """
        Remove a track object from the song.
        """
        self.tracks = [ t for t in self.tracks if t.obj_id != track.obj_id ]

    def add_scenes(self, scenes):
        """
        Adds some scene objects to the song.
        """
        self.scenes.extend(scenes)

    def remove_scene(self, scene):
        """
        Removes a scene object from the song.
        """
        self.scenes = [ s for s in self.scenes if s.obj_id != scene.obj_id ]

    def add_patterns(self, patterns):
        """
        Adds some pattern objects to the song.
        """
        for x in patterns:
            self.patterns[str(x.obj_id)] = x

    def remove_pattern(self, pattern):
        """
        Removes a pattern object from the song.
        """
        del self.patterns[str(pattern.obj_id)]

    def add_data_pools(self, data_pools):
        """
        Adds some pattern objects to the song.
        """
        for x in data_pools:
            self.data_pools[str(x.obj_id)] = x

    def remove_data_pool(self, data_pool):
        """
        Removes a pattern object from the song.
        """
        del self.data_pools[str(data_pool.obj_id)]

    def add_transforms(self, transforms):
        """
        Adds some transform objects to the song.
        """
        for x in transforms:
            self.transforms[str(x.obj_id)] = x

    def remove_transform(self, transform):
        """
        Removes a transform object from the song.
        """
        del self.transforms[str(transform.obj_id)]

    def get_web_grid(self):

        # this returns grid info for UI display

        columns = []

        columns.append(dict(
           headerName="Scene",
           field="scene",
           editable=False,
           rowDrag=True,
           rowDragText="Scene"
        ))

        for t in self.tracks:
            columns.append(dict(
                headerName=t.name,
                field=t.name,
                editable=False,
                headerComponentParams=(dict(template=TRACK_HEADER_TEMPLATE % t.obj_id)),
            ))

        rows = []
        for s in self.scenes:
            row = dict()
            row['scene'] = dict(type='scene', scene_id=s.obj_id, scene_name=s.name)
            for t in self.tracks:
                clip = self.get_clip_for_scene_and_track(scene=s, track=t)
                if clip:
                    row[t.name] = dict(type='clip', track_id=t.obj_id, scene_id=s.obj_id, clip_id=clip.obj_id, clip_name=clip.name)
                else:
                    row[t.name] = dict(type='empty_cell', track_id=t.obj_id, scene_id=s.obj_id)
            rows.append(row)

        result = dict(
            column_defs = columns,
            row_data = rows
        )

        return result

    def update_scene_order_for_ui(self, data):

        scene_ids = [ x["scene"]["scene_id"] for x in data ]
        scenes = [ self.find_scene(x) for x in scene_ids ]
        self.scenes = scenes
        return True

    def delete_web_rows(self, data):

        results = []
        for (i,x) in enumerate(self.scenes):
            if i not in data:
                results.append(x)
        self.scenes = results
        return True

