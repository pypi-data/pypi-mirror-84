# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.slot import DataSlot
import traceback



class DataSlotCompiler(object):

    __slots__ = ()

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def get_grid(self, web_slots):

        return dict(
            column_defs = self._get_column_defs(),
            row_data = self._get_row_data(web_slots)
        )

    # ------------------------------------------------------------------------------------------------------------------

    def _get_column_defs(self):

        results = []

        results.append(dict(
            headerName = "slot",
            valueGetter = "node.rowIndex + 1"
        ))

        results.append(dict(
            headerName = "Value",
            field = "value",
            editable = True
        ))

        return results

    # ------------------------------------------------------------------------------------------------------------------

    def _get_row_data(self, web_slots):

        results = []

        web_slot_items = web_slots

        if web_slot_items is None:
            web_slot_items = []

        for web_slot in web_slot_items:
            item = dict()
            item['value'] = web_slot.get('value', None)
            results.append(item)

        return results

    # ------------------------------------------------------------------------------------------------------------------

    def update_web_slots_from_ui(self, web_slots, data):

        results = []

        existing_length = len(web_slots)

        for (i,x) in enumerate(data):
            if i < existing_length:
                item = web_slots[i]
            else:
                item = dict()
            item.update(x)
            results.append(item)

        new_length = len(data)
        if existing_length > new_length:
            results = results[:new_length-1]
        return results

    # ------------------------------------------------------------------------------------------------------------------

    def compile(self, web_slots):

        results = []
        errors = []

        for (i,x) in enumerate(web_slots):

            slot = DataSlot()
            slot.value = x.get("value",0)
            results.append(slot)

        if len(errors):
            return (False, results, errors)
        else:
            return (True, results, errors)

