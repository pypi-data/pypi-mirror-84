# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, button

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
}
"""

SIDE_HTML = """
<font color='blue'><i class="fas fa-plug fa-4x" aria-hidden="true"></i></font>
"""

class DeviceBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
             textbox(data, "Device", "new_name", disabled=True)
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return [
            button(caption="Close", fa_class="far", fa_icon="fa-window-close", onclick="close_workspace()"),
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS

    @classmethod
    def side_html(self):
        return SIDE_HTML