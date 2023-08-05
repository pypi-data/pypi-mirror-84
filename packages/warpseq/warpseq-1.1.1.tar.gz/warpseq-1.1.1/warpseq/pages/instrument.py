# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, button, rangebox, toggle
from warpseq.model.note import NOTES

CUSTOM_JS = """

function intercept_field(field,value) {
   return true;
}

function edit_this() {
  edit_instrument();
}
"""

SIDE_HTML = """
<font color='blue'><i class="fas fa-digital-tachograph fa-4x" aria-hidden="true"></i></font>
"""

CHANNELS = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
OCTAVES = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]

class InstrumentBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_button_parameters(cls, data):
        return [
            button(caption="Copy", link_class="blue_on_hover", fa_icon="fa-copy", onclick="copy_instrument()"),
            button(caption="Delete",link_class="red_on_hover", fa_class="far", fa_icon="fa-trash-alt", onclick="delete_instrument()"),
            button(caption="Close", link_class="blue_on_hover", fa_class="far", fa_icon="fa-window-close", onclick="close_workspace()"),
        ]
    # TODO: should maybe default 'device' to the first device?

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Instrument", "new_name"),
            select(data, "Device", "device", choices="devices", nullable=True),
            select(data, "Channel", "channel", choices=CHANNELS, nullable=False),
            rangebox(data, "Min Octave", "min_octave", min=0, max=8, step=1, use_default=1),
            rangebox(data, "Base Octave", "base_octave", min=0, max=8, step=1, use_default=1),
            rangebox(data, "Max Octave", "max_octave", min=0, max=8, step=1, use_default=1),
            rangebox(data, "Default Velocity", "default_velocity", min=0, max=127, step=1, use_default=120),
            toggle(data, "Muted", "muted"),
            select(data, "Drum 1 Note", "drum1_note", choices=NOTES, nullable=False),
            select(data, "Drum 1 Octave", "drum1_octave", choices=OCTAVES, nullable=False),
            select(data, "Drum 2 Note", "drum2_note", choices=NOTES, nullable=False),
            select(data, "Drum 2 Octave", "drum2_octave", choices=OCTAVES, nullable=False),
            select(data, "Drum 3 Note", "drum3_note", choices=NOTES, nullable=False),
            select(data, "Drum 3 Octave", "drum3_octave", choices=OCTAVES, nullable=False),
            select(data, "Drum 4 Note", "drum4_note", choices=NOTES, nullable=False),
            select(data, "Drum 4 Octave", "drum4_octave", choices=OCTAVES, nullable=False),
            select(data, "Drum 5 Note", "drum5_note", choices=NOTES, nullable=False),
            select(data, "Drum 5 Octave", "drum5_octave", choices=OCTAVES, nullable=False),
            select(data, "Drum 6 Note", "drum6_note", choices=NOTES, nullable=False),
            select(data, "Drum 6 Octave", "drum6_octave", choices=OCTAVES, nullable=False),
            select(data, "Drum 7 Note", "drum7_note", choices=NOTES, nullable=False),
            select(data, "Drum 7 Octave", "drum7_octave", choices=OCTAVES, nullable=False),
            select(data, "Drum 8 Note", "drum8_note", choices=NOTES, nullable=False),
            select(data, "Drum 8 Octave", "drum8_octave", choices=OCTAVES, nullable=False),
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS

    @classmethod
    def side_html(self):
        return SIDE_HTML