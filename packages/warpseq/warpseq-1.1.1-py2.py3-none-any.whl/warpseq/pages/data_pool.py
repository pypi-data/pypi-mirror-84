# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.pages.base import BaseBuilder
from warpseq.server.widgets import textbox, select, multiple, button, rangebox, toggle
from warpseq.model.directions import DIRECTIONS

CUSTOM_JS = """
function intercept_field(field,value) {
   return true;
}
function edit_this() {
  edit_data_pool();
}

load_data_pool_grid();
"""

SIDE_HTML = """
<font color='purple'><i class="fas fa-database fa-4x" aria-hidden="true"></i></font>
"""

class DataPoolBuilder(BaseBuilder):

    __slots__ = ()

    @classmethod
    def get_form_parameters(cls, data):
        return [
            textbox(data, "Data Pool", "new_name"),
            select(data, "Direction", "direction", choices=DIRECTIONS, nullable=False),
        ]

    @classmethod
    def get_button2_parameters(self, data):
        return [
            button(caption="1", link_class="blue_on_hover", fa_icon="fa-plus", id="new_row_button"),
            button(caption="4", link_class="blue_on_hover",  fa_icon="fa-plus", id="new_row4_button"),
            button(caption="8", link_class="blue_on_hover", fa_icon="fa-plus", id="new_row8_button"),
            button(caption="Delete Selected", link_class="blue_on_hover",  fa_icon="fa-times", id="delete_row_button"),
        ]

    @classmethod
    def get_button_parameters(cls, data):
        return [
            button(caption="Copy Data Pool", link_class="blue_on_hover", fa_icon="fa-copy", onclick="copy_data_pool()"),
            button(caption="Delete", link_class="red_on_hover", fa_class="far", fa_icon="fa-trash-alt", onclick="delete_data_pool()"),
            button(caption="Close", link_class="blue_on_hover", fa_class="far", fa_icon="fa-window-close", onclick="close_workspace()"),
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