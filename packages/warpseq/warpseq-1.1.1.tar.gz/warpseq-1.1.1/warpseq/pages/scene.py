# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, toggle, rangebox, button

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_scene();
}
"""

SIDE_HTML = """
<font color='green'><i class="fas fa-mountain fa-4x" aria-hidden="true"></i></font>
"""

class SceneBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Scene", "new_name"),
            textbox(data, "Rate", "rate"),
            toggle(data, "Auto Advance", "auto_advance"),
            select(data, "Scale", "scale", choices="scales", nullable=True)
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return [
            button(caption="Copy", link_class="blue_on_hover", fa_icon="fa-copy", onclick="copy_scene()"),
            button(caption="Delete", link_class="red_on_hover", fa_class="far", fa_icon="fa-trash-alt", onclick="delete_scene()"),
            button(caption="Close", link_class="blue_on_hover", fa_class="far", fa_icon="fa-window-close", onclick="close_workspace()"),
        ]

    @classmethod
    def get_custom_js(cls):
        return CUSTOM_JS

    @classmethod
    def side_html(self):
        return SIDE_HTML