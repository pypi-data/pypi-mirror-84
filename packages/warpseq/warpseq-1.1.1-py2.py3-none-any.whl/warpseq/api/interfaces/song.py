# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

import json
from warpseq.utils.cast import safe_int

class SongApi(object):

    def __init__(self, public_api, song):
        self.public_api = public_api
        self.song = song

    def edit(self, name:str=None, new_name:str=None, id:str=None, filename:str=None, tempo:int=None, scale:str=None):
        # id is ignored, because there is only one song.
        if tempo:
            tempo = safe_int(tempo, 120)
            if tempo < 1:
                tempo = 1
            if tempo > 400:
                tempo = 400
            self.song.tempo = tempo

        if scale:
            scale = self.public_api.scales.lookup(scale, require=True, field="scale")
            self.song.scale = scale
        if name:
            self.song.name = name
        if new_name:
            self.song.name = new_name
        if filename:
            self.song.filename = filename

    def details(self):
        return self.song.details()

    def to_dict(self):
        return self.song.to_dict()

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    def get_web_grid(self):
        return self.song.get_web_grid()

    def update_scene_order_for_ui(self, data):
        return self.song.update_scene_order_for_ui(data)

    def delete_web_rows(self, data):
        return self.song.delete_web_rows(data)

    def status_report(self):
        return self.song.status_report()