# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, rangebox, button
from warpseq.model.scale import SCALE_TYPE_NAMES

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_song();
}

load_song_grid();
"""

SIDE_HTML = """
<font color='green'><i class="fas fa-compact-disc fa-4x" aria-hidden="true"></i></font>
"""

BONUS_HTML = ""

class SongBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Song", "new_name"),
            textbox(data, "Filename", "filename"),
            # textbox(data, "Tempo", "tempo"),
            rangebox(data, "Tempo", "tempo", min=1, max=400, step=1, use_default=120),
            select(data, "Scale", "scale", choices="scales", nullable=True)
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return [
            button(caption="Open Song", link_class="blue_on_hover", fa_class='far', fa_icon="fa-folder-open", onclick="file_load()"),
            button(caption="Save Song", link_class="blue_on_hover",  fa_class='far', fa_icon="fa-save", onclick="file_save_as()"),
            button(caption="Init Song", link_class="red_on_hover", fa_class="fas", fa_icon="fa-radiation", onclick="file_new()"),
        ]

    @classmethod
    def get_button2_parameters(self, data):
        return [
            button(caption="Play", link_class="green_on_hover", fa_icon="fa-play", id="song_global_play_button", onclick="play()"),
            button(caption="Stop", link_class="red_on_hover", fa_icon="fa-stop", id="song_global_stop_button", onclick="stop()"),
            # button(caption="Panic", link_class="blue_on_hover", fa_icon="fa-exclamation-circle", fa_class='fas', id="song_midi_panic_button", onclick="midi_panic()"),
            button(caption="Add Scene", link_class="blue_on_hover", fa_icon="fa-plus", id="new_scene_button"),
            button(caption="Add Track", link_class="blue_on_hover",  fa_icon="fa-plus", id="new_track_button"),
            button(caption="Delete Selected Scenes", link_class="red_on_hover",  fa_icon="fa-times", id="delete_scene_button"),
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS

    @classmethod
    def has_grid(self):
        return True

    @classmethod
    def side_html(self):
        return SIDE_HTML

    @classmethod
    def bonus_html(self):
        return BONUS_HTML