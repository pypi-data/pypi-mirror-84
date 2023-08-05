# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

# the api router decides what API calls to make for incoming
# service packet requests

from warpseq.server.packet import ResponsePacket
from warpseq.api.exceptions import InvalidOpcode, StopException
import traceback
from warpseq.model.note import NOTES, SCALE_DEGREES_FOR_UI
from warpseq.model.scale import SCALE_TYPES

# ======================================================================================================================

class ModelRouter(object):

    __slots__ = ('api','callbacks','engine')

    def __init__(self, api, engine, callbacks=None):
        self.api = api
        self.callbacks = callbacks
        self.engine = engine

    # ------------------------------------------------------------------------------------------------------------------

    def dispatch(self, original_message, pkt):

        if pkt.cmd != 'status_report':
            print("req: %s" % pkt.to_dict())

        try:

            fn = getattr(self, "FN_%s" % pkt.cmd, None)

            if fn is None:
                raise InvalidOpcode()

            data = fn(pkt)

            return ResponsePacket(ok=True, data=data)

        except Exception as e:

            print("... failed ... ")
            traceback.print_exc()

            return ResponsePacket(ok=False, msg=str(e))

    # ------------------------------------------------------------------------------------------------------------------

    def FN_list_device(self, pkt):
        return sorted(self.api.devices.list(), key=namesort)

    def FN_list_instrument(self, pkt):
        return sorted(self.api.instruments.list(), key=namesort)

    def FN_list_track(self, pkt):
        return self.api.tracks.list(show_hidden=False)

    def FN_list_scene(self, pkt):
        return self.api.scenes.list(show_hidden=False)

    def FN_list_pattern(self, pkt):
        return sorted(self.api.patterns.list(), key=namesort)

    def FN_list_data_pool(self, pkt):
        return sorted(self.api.data_pools.list(), key=namesort)

    def FN_list_scale(self, pkt):
        return sorted(self.api.scales.list(), key=namesort)

    def FN_list_transform(self, pkt):
        return sorted(self.api.transforms.list(), key=namesort)

    # ------------------------------------------------------------------------------------------------------------------

    def FN_get_song(self, pkt):
        return self._with_choices(self.api.song.details())

    def FN_get_device(self, pkt):
        return self._with_choices(self.api.devices.details(id=pkt.id))

    def FN_get_scene(self, pkt):
        return self._with_choices(self.api.scenes.details(id=pkt.id))

    def FN_get_scale(self, pkt):
        return self._with_choices(self.api.scales.details(id=pkt.id))

    def FN_get_instrument(self, pkt):
        return self._with_choices(self.api.instruments.details(id=pkt.id))

    def FN_get_track(self, pkt):
        return self._with_choices(self.api.tracks.details(id=pkt.id))

    def FN_get_pattern(self, pkt):
        return self._with_choices(self.api.patterns.details(id=pkt.id))

    def FN_get_transform(self, pkt):
        return self._with_choices(self.api.transforms.details(id=pkt.id))

    def FN_get_data_pool(self, pkt):
        return self._with_choices(self.api.data_pools.details(id=pkt.id))

    def FN_get_clip(self, pkt):
        (scene, track) = pkt.id.split(",")
        scene = self.api.scenes.lookup(id=scene)
        track = self.api.tracks.lookup(id=track)
        clip = self.api.song.song.get_clip_for_scene_and_track(scene, track)
        details = self.api.clips.details(id=clip.obj_id)
        extended = self._with_choices(details)
        return extended

    def _with_choices(self, data):
        data["choices"] = self.get_choices()
        return data

    # ------------------------------------------------------------------------------------------------------------------

    def FN_grid_for_song(self, pkt):
        return self.api.song.get_web_grid()

    def FN_grid_for_song_postback(self, pkt):
        return self.api.song.update_scene_order_for_ui(data=pkt.data)

    def FN_grid_for_pattern_postback(self, pkt):
        return self.api.patterns.update_web_slots_for_ui(id=pkt.id, data=pkt.data)

    def FN_grid_for_transform_postback(self, pkt):
        return self.api.transforms.update_web_slots_for_ui(id=pkt.id, data=pkt.data)

    def FN_grid_for_data_pool_postback(self, pkt):
        return self.api.data_pools.update_web_slots_for_ui(id=pkt.id, data=pkt.data)

    def FN_grid_for_pattern(self, pkt):
        return self.api.patterns.get_web_slot_grid_for_ui(id=pkt.id, category=pkt.data['category'])

    def FN_grid_for_transform(self, pkt):
        return self.api.transforms.get_web_slot_grid_for_ui(id=pkt.id, category=pkt.data['category'])

    def FN_grid_for_data_pool(self, pkt):
        return self.api.data_pools.get_web_slot_grid_for_ui(id=pkt.id)

    def FN_grid_for_pattern_delete_rows(self, pkt):
        return self.api.patterns.delete_web_slot_rows(id=pkt.id, data=pkt.data)

    def FN_grid_for_transform_delete_rows(self, pkt):
        return self.api.transforms.delete_web_slot_rows(id=pkt.id, data=pkt.data)

    def FN_grid_for_data_pool_delete_rows(self, pkt):
        return self.api.data_pools.delete_web_slot_rows(id=pkt.id, data=pkt.data)

    def FN_grid_for_song_delete_rows(self, pkt):
        return self.api.song.delete_web_rows(data=pkt.data)

    def FN_grid_for_clip(self, pkt):
        return self.api.clips.get_web_slot_grid_for_ui(id=pkt.id)

    def FN_grid_for_clip_postback(self, pkt):
        return self.api.clips.update_web_slot_grid_for_ui(id=pkt.id, data=pkt.data)


    # ------------------------------------------------------------------------------------------------------------------

    def FN_delete_scale(self, pkt):
        return self.api.scales.delete(id=pkt.id)

    def FN_delete_instrument(self, pkt):
        return self.api.instruments.delete(id=pkt.id)

    def FN_delete_scene(self, pkt):
        return self.api.scenes.delete(id=pkt.id)

    def FN_delete_track(self, pkt):
        return self.api.tracks.delete(id=pkt.id)

    def FN_delete_pattern(self, pkt):
        return self.api.patterns.delete(id=pkt.id)

    def FN_delete_transform(self, pkt):
        return self.api.transforms.delete(id=pkt.id)

    def FN_delete_data_pool(self, pkt):
        return self.api.data_pools.delete(id=pkt.id)

    def FN_delete_clip(self, pkt):
        return self.api.clips.delete(id=pkt.id)

    # ------------------------------------------------------------------------------------------------------------------

    def FN_copy_scale(self, pkt):
        return self.api.scales.copy(id=pkt.id)

    def FN_copy_instrument(self, pkt):
        return self.api.instruments.copy(id=pkt.id)

    def FN_copy_scene(self, pkt):
        return self.api.scenes.copy(id=pkt.id)

    def FN_copy_track(self, pkt):
        return self.api.tracks.copy(id=pkt.id)

    def FN_copy_pattern(self, pkt):
        return self.api.patterns.copy(id=pkt.id)

    def FN_copy_transform(self, pkt):
        return self.api.transforms.copy(id=pkt.id)

    def FN_copy_data_pool(self, pkt):
        return self.api.data_pools.copy(id=pkt.id)

    def FN_copy_clip(self, pkt):
        return self.api.clips.copy(id=pkt.id)

    # ------------------------------------------------------------------------------------------------------------------

    def get_choices(self):
        choices = dict(
            scales = self.api.scales.list(),
            devices = self.api.devices.list(),
            instruments = self.api.instruments.list(),
            patterns = self.api.patterns.list(),
            notes = NOTES,
            scale_types = [ x for x in SCALE_TYPES.keys() ],
            scale_degrees = [x for x in SCALE_DEGREES_FOR_UI ],
        )
        return choices

    # ------------------------------------------------------------------------------------------------------------------

    def FN_edit_song(self, pkt):
        return self.api.song.edit(**pkt.data)

    def FN_edit_scale(self, pkt):
        return self.api.scales.edit(**pkt.data)

    def FN_edit_instrument(self, pkt):
        return self.api.instruments.edit(**pkt.data)

    def FN_edit_scene(self, pkt):
        return self.api.scenes.edit(**pkt.data)

    def FN_edit_track(self, pkt):
        return self.api.tracks.edit(**pkt.data)

    def FN_edit_pattern(self, pkt):
        return self.api.patterns.edit(**pkt.data)

    def FN_edit_transform(self, pkt):
        return self.api.transforms.edit(**pkt.data)

    def FN_edit_data_pool(self, pkt):
        return self.api.data_pools.edit(**pkt.data)

    def FN_edit_clip(self, pkt):
        return self.api.clips.edit(**pkt.data)

    # ------------------------------------------------------------------------------------------------------------------

    def FN_new_instrument(self, pkt):
        return self.api.instruments.create()

    def FN_new_track(self, pkt):
        return self.api.tracks.create()

    def FN_new_scene(self, pkt):
        return self.api.scenes.create()

    def FN_new_clip(self, pkt):
        return self.api.clips.create()

    def FN_new_transform(self, pkt):
        return self.api.transforms.create()

    def FN_new_data_pool(self, pkt):
        return self.api.data_pools.create()

    def FN_new_scale(self, pkt):
        return self.api.scales.create()

    def FN_new_pattern(self, pkt):
        return self.api.patterns.create()

    def FN_new_clip(self, pkt):
        scene_id = pkt.data["scene_id"]
        track_id = pkt.data["track_id"]
        return self.api.clips.create(scene_id, track_id)

    # ------------------------------------------------------------------------------------------------------------------

    def FN_file_new(self, pkt):
        self.api.reset()
        return True

    def FN_data_load(self, pkt):
        self.api.reset()
        self.api.from_json(pkt.data["file_contents"])
        return True

    def FN_file_save(self, pkt):
        return self.api.to_dict()

    def FN_status_report(self, pkt):
        return self.api.song.status_report()

    # ------------------------------------------------------------------------------------------------------------------

    def FN_play_scene(self, pkt):
        self.api.player.add_scene_id(pkt.id)

    def FN_stop_track(self, pkt):
        self.api.player.stop_track_id(pkt.id)

    def FN_play_clip(self, pkt):
        self.api.player.add_clip_ids([pkt.id])

    def FN_play_scene(self, pkt):
        self.api.player.add_scene_id(pkt.id)

    def FN_audition_pattern(self, pkt):
        self.api.player.audition_pattern_id(pkt.id)

    def FN_audition_transform(self, pkt):
        self.api.player.audition_transform_id(pkt.id)

    def FN_audition_clip(self, pkt):
        self.api.player.audition_clip_id(pkt.id)

    def FN_audition_clip_slot(self, pkt):
        self.api.player.audition_clip_slot(pkt.data['clip_id'], pkt.data['slot_number'])

    def FN_play(self, pkt):
        self.api.player.add_first_scene()

    def FN_stop(self, pkt):
        self.api.player.stop()

def namesort(x):
    return x["name"]