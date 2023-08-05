# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, button, rangebox, toggle, spacer
from warpseq.model.directions import DIRECTIONS
from warpseq.model.pattern import PATTERN_TYPES, STANDARD

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_pattern();
}

load_pattern_common_grid();

$("#pattern_type").on('select2:select', function (e) {
   load_pattern_common_grid(); 
});
 
"""

SIDE_HTML = """
<font color='purple'><i class="fas fa-stroopwafel fa-4x" aria-hidden="true"></i></font>
"""

class PatternBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Pattern", "new_name"),
            rangebox(data, "Octave shift", "octave_shift", min=-5, max=+5, use_default=0, step=1),
            textbox(data, "Rate", "rate"),
            select(data, "Scale", "scale", choices="scales", nullable=True),
            select(data, "Direction", "direction", choices=DIRECTIONS, nullable=False),
            select(data, "Pattern Type", "pattern_type", choices=PATTERN_TYPES, nullable=False),
            select(data, "Drum Config", "drum_config", choices="instruments", nullable=True),
            select(data, "Audition With", "audition_with", choices="instruments", nullable=True)
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return [

            button(caption="Copy", link_class="blue_on_hover", fa_icon="fa-copy", onclick="copy_pattern()"),
            button(caption="Delete", link_class="red_on_hover", fa_class="far", fa_icon="fa-trash-alt", onclick="delete_pattern()"),
            button(caption="Close", link_class="blue_on_hover", fa_class="far", fa_icon="fa-window-close", onclick="close_workspace()"),
        ]

    @classmethod
    def get_button2_parameters(self, data):
        return [
            button(caption="Audition", link_class="green_on_hover", fa_icon="fa-play", onclick="audition_pattern()"),
            button(caption="Stop", link_class="red_on_hover", fa_icon="fa-stop", onclick="stop()"),
            spacer(),

            button(caption="Main", div_id="pattern_common", div_class="button_tab button_tab_active", link_class="blue_on_hover", fa_icon="fa-star", onclick="load_pattern_common_grid()"),
            button(caption="Pitch", div_id="pattern_pitch", div_class="button_tab", link_class="blue_on_hover", fa_icon="fa-music", onclick="load_pattern_pitch_grid()"),
            button(caption="Time", div_id="pattern_time", div_class="button_tab", link_class="blue_on_hover", fa_icon="fa-clock", fa_class="far", onclick="load_pattern_time_grid()"),
            button(caption="Mod", div_id="pattern_mod", div_class="button_tab", link_class="blue_on_hover", fa_icon="fa-random", onclick="load_pattern_modulation_grid()"),
            button(caption="Vars", div_id="pattern_vars", div_class="button_tab", link_class="blue_on_hover", fa_icon="fa-calculator", onclick="load_pattern_variable_grid()"),
            button(caption="Control", div_id="pattern_ctrl", div_class="button_tab", link_class="blue_on_hover", fa_icon="fa-arrows-alt", fa_class="fas", onclick="load_pattern_control_grid()"),
            spacer(),

            button(caption="1", link_class="blue_on_hover", fa_icon="fa-plus", id="new_row_button"),
            button(caption="4", link_class="blue_on_hover", fa_icon="fa-plus", id="new_row4_button"),
            button(caption="8", link_class="blue_on_hover", fa_icon="fa-plus", id="new_row8_button"),
            button(caption="Delete Selected", link_class="blue_on_hover", fa_icon="fa-times", id="delete_row_button"),
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