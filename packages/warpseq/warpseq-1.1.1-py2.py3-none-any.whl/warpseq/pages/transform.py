# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, rangebox, button, toggle, spacer
from warpseq.model.transform import APPLIES_CHOICES
from warpseq.model.directions import DIRECTIONS

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_transform();
}

load_transform_pitch_grid();

"""

SIDE_HTML = """
<font color='purple'><i class="fas fa-frog fa-4x" aria-hidden="true"></i></font>
"""

DIVIDE = [ "auto", "1", "2", "3", "4", "5", "6", "7", "8" ]

class TransformBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Transform", "new_name"),
            toggle(data, "Arpeggiate", "arp"),
            select(data, "Divide", "divide", choices=DIVIDE, nullable=True),
            select(data, "Applies To", "applies_to", choices=APPLIES_CHOICES),
            select(data, "Direction", "direction", choices=DIRECTIONS, nullable=False),
            toggle(data, "Auto Reset", "auto_reset"),
            select(data, "Audition Instrument", "audition_instrument", choices="instruments", nullable=True),
            select(data, "Audition Pattern", "audition_pattern", choices="patterns", nullable=True),

        ]

    @classmethod
    def get_button_parameters(cls, data):
        return [

            button(caption="Copy", link_class="blue_on_hover", fa_icon="fa-copy", onclick="copy_transform()"),
            button(caption="Delete", link_class="red_on_hover", fa_class="far", fa_icon="fa-trash-alt", onclick="delete_transform()"),
            button(caption="Close", link_class="blue_on_hover", fa_class="far", fa_icon="fa-window-close", onclick="close_workspace()"),
        ]

    @classmethod
    def get_button2_parameters(self, data):
        return [
            button(caption="Audition", fa_icon="fa-play", link_class='green_on_hover', onclick="audition_transform()"),
            button(caption="Stop", fa_icon="fa-stop", link_class='red_on_hover', onclick="stop()"),
            spacer(),

            button(caption="Main", div_id="transform_pitch", div_class="button_tab button_tab_active", link_class="blue_on_hover", fa_icon="fa-music", onclick="load_transform_pitch_grid()"),
            button(caption="Time", div_id="transform_time", div_class="button_tab", link_class="blue_on_hover", fa_icon="fa-clock", fa_class="far", onclick="load_transform_time_grid()"),
            button(caption="Mod", div_id="transform_mod", div_class="button_tab", link_class="blue_on_hover", fa_icon="fa-random", onclick="load_transform_modulation_grid()"),
            button(caption="Vars", div_id="transform_vars", div_class="button_tab", link_class="blue_on_hover", fa_icon="fa-calculator", onclick="load_transform_variable_grid()"),
            button(caption="Control", div_id="transform_ctrl", div_class="button_tab", link_class="blue_on_hover", fa_icon="fa-arrows-alt", fa_class="fas", onclick="load_transform_control_grid()"),
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