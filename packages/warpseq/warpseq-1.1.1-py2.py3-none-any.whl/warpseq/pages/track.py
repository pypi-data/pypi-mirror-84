# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, toggle, rangebox, button
from warpseq.model.track import INSTRUMENT_MODE_CHOICES

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_track();
}
"""

SIDE_HTML = """
<font color='green'><i class="fas fa-wave-square fa-4x" aria-hidden="true"></i></font>
"""

class TrackBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Track", "new_name"),
            toggle(data, "Muted", "muted"),
            multiple(data, "Instruments", "instruments", choices="instruments", nullable=True),
            select(data, "Instrument Mode", "instrument_mode", choices=INSTRUMENT_MODE_CHOICES, nullable=False),
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return [
            button(caption="Copy", link_class="blue_on_hover", fa_icon="fa-copy", onclick="copy_this()"),
            button(caption="Delete", link_class="red_on_hover", fa_class="far", fa_icon="fa-trash-alt", onclick="delete_track()"),
            button(caption="Close", link_class="blue_on_hover", fa_class="far", fa_icon="fa-window-close", onclick="close_workspace()"),
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS

    @classmethod
    def side_html(self):
        return SIDE_HTML