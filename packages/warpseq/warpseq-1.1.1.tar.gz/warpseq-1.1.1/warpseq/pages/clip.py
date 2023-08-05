# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, button, rangebox, toggle, infobox
from warpseq.model.directions import DIRECTIONS


CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_clip();
}

load_clip_grid();

//$("#pattern_type").on('select2:select', function (e) {
//   load_pattern_common_grid(); 
//});
//load_clip_pattern_grid();
//load_clip_transform_grid();
//load_clip_scale_grid();
//load_clip_tempo_shift_grid();

"""

BONUS_HTML = """
"""

SIDE_HTML = """
<font color='green'><i class="fas fa-paperclip fa-4x" aria-hidden="true"></i></font>
"""

class ClipBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Clip", "new_name"),
            infobox(data, "Scene", "scene"),
            infobox(data, "Track", "track"),
            textbox(data, "Rate", "rate"),
            textbox(data, "Cycle Limit", "repeat"),
            toggle(data, "Advance Scene", "auto_scene_advance"),
        ]

    @classmethod
    def get_button2_parameters(self, data):
        return [
            button(caption="Audition", link_class='green_on_hover', fa_icon="fa-play", onclick="audition_clip()"),
            button(caption="Stop", link_class='red_on_hover', fa_icon="fa-stop", onclick="stop()"),
            button(caption="Delete", fa_icon="fa-times", id="delete_row_button"),
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return [
            button(caption="Delete", link_class="red_on_hover", fa_class="far", fa_icon="fa-trash-alt", onclick="delete_clip()"),
            button(caption="Close", link_class="blue_on_hover", fa_class="far", fa_icon="fa-window-close", onclick="load_song()"),
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS

    @classmethod
    def has_grid(self):
        return True

    @classmethod
    def bonus_html(self):
        return BONUS_HTML

    @classmethod
    def side_html(self):
        return SIDE_HTML