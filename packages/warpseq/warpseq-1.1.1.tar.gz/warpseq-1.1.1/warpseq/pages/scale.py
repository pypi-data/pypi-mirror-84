# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, button

CUSTOM_JS = """

function intercept_field(field,value) {
   if (field == 'slots') {
       clear_scale_type();
   } else if (field == 'scale_type') {
       clear_slots();
   }
   return true;
}

function edit_this() {
  edit_scale();
}
"""

SIDE_HTML = """
<font color='blue'><i class="fas fa-music fa-4x" aria-hidden="true"></i></font>
"""

class ScaleBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_button_parameters(cls, data):
        return [
            button(caption="Copy", link_class="blue_on_hover", fa_icon="fa-copy", onclick="copy_scale()"),
            button(caption="Delete", link_class="red_on_hover", fa_class="far", fa_icon="fa-trash-alt", onclick="delete_scale()"),
            button(caption="Close", link_class="blue_on_hover", fa_class="far", fa_icon="fa-window-close", onclick="close_workspace()"),
        ]

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Scale", "new_name"),
            select(data, "Root", "note", choices="notes"),
            select(data, "Type", "scale_type", choices="scale_types", nullable=True),
            multiple(data, "Degrees", "slots", choices="scale_degrees", nullable=True)
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS

    @classmethod
    def side_html(self):
        return SIDE_HTML