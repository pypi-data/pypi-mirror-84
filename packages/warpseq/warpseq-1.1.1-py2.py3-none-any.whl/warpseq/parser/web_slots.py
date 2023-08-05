# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.slot import Slot
from warpseq.model.evaluator import RandomRange, RandomChoice, Probability, DataGrab, LoadVariable
from warpseq.utils.cast import safe_int

import traceback


CATEGORY_COMMON = 'common'
CATEGORY_PITCH = 'pitch'
CATEGORY_TIME = 'time'
CATEGORY_MOD = 'modulation'
CATEGORY_CONTROL = 'control'
CATEGORY_VARIABLES = 'variable'

# column fields

INST_COMMON = [ "degree", "octave_shift", "chord_type", "length", "repeats", "velocity" ]
DRUM_COMMON = [ "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8" ]
INST_PITCH = [ "sharp", "flat", "inversion", "degree_shift" ]
DRUM_PITCH = [ ]

TRANSFORM_PITCH = [ "degree_shift", "octave_shift", "sharp", "flat", "chord_type", "inversion" ]
TIME = [ "rest", "tie", "delay", "skip" ]
VARIABLES = [ "v_a", "v_a_value", "v_b", "v_b_value", "v_c", "v_c_value", "v_d", "v_d_value" ]
MODULATION = [ "cc_a", "cc_a_value", "cc_b", "cc_b_value", "cc_c", "cc_c_value", "cc_d", "cc_d_value" ]
CONTROL = [ "track_grab", "shuffle", "reverse", "reset", "skip" ]

# header names for columns

HEADER_NAMES = {
   "D1": "D1",
   "D2": "D2",
   "D3": "D3",
   "D4": "D4",
   "D5": "D5",
   "D6": "D6",
   "D7": "D7",
   "D8": "D8",
   "degree": "Degree",
   "chord_type" : "Chord Type",
   "sharp" : "# *",
   "flat" : "b *",
   "degree_shift" : "Degree +/-",
   "octave_shift" : "Octave +/-",
   "note" : "Note",
   "octave" : "Octave",
   "length" : "Length",
   "repeats" : "Repeat",
   "delay" : "Delay",
   "rest" : "Rest *",
   "velocity" : "Velocity",
   "v_a" : "Var A",
   "v_a_value" : "=",
   "v_b" : "Var B",
   "v_b_value" : "=",
   "v_c" : "Var C",
   "v_c_value" : "=",
   "v_d" : "Var D",
   "v_d_value" : "=",
   "cc_a" : "CC A",
   "cc_b": "CC B",
   "cc_c": "CC C",
   "cc_d": "CC D",
   "cc_a_value" : "=",
   "cc_b_value": "=",
   "cc_c_value": "=",
   "cc_d_value": "=",
   "shuffle" : "Shuffle *",
   "reverse" : "Reverse *",
   "reset" : "Reset *",
   "tie" : "Tie *",
   "track_grab" : "Track Grab",
   "skip" : "Skip",
   "inversion": "Inversion"
}

ALL_COLUMNS =[x for x in HEADER_NAMES.keys() ]
INT_COLUMNS = [ "degree", "degree_shift", "octave_shift", "octave", "repeats", "velocity", "inversion", "skip" ]
CC_KEYS = [ "cc_a_value", "cc_b_value", "cc_c_value", "cc_d_value", "cc_a", "cc_b", "cc_c", "cc_d"]
VARIABLE_KEYS = [ "v_a_value", "v_b_value", "v_c_value", "v_d_value", "v_a", "v_b", "v_c", "v_d" ]
FLOAT_COLUMNS = [ "length", "delay" ]
BOOL_COLUMNS = [ "sharp", "flat", "rest", "shuffle", "reverse", "reset", "tie", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8" ]
STR_COLUMNS = [ "chord_type", "note", "track_grab" ]
DICT_COLUMNS = [ "variables", "ccs" ]

# ======================================================================================================================


class WebSlotCompiler(object):

    __slots__ = ('for_transform', 'pattern_type')

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, for_transform=False, pattern_type=None):

        self.for_transform = for_transform
        self.pattern_type = pattern_type

    # ------------------------------------------------------------------------------------------------------------------

    def get_grid(self, web_slots, category):

        columns = self._get_columns_for_categories(category)
        result = dict(
            column_defs = self._get_column_defs(columns),
            row_data = self._get_row_data(web_slots, columns)
        )
        return result

    # ------------------------------------------------------------------------------------------------------------------

    def _get_column_defs(self, columns):



        results = []

        results.append(dict(
            headerName = "slot",
            valueGetter = "node.rowIndex + 1"
        ))

        for x in columns:
            results.append(dict(
                headerName = HEADER_NAMES[x],
                field = x,
                editable = True,
            ))
        return results

    # ------------------------------------------------------------------------------------------------------------------

    def _get_row_data(self, web_slots, columns):

        results = []

        web_slot_items = web_slots
        if web_slot_items is None:
            web_slot_items = []

        for web_slot in web_slot_items:
            item = {}
            for column in columns:
                item[column] = web_slot.get(column, None)

            results.append(item)

        return results

    # ------------------------------------------------------------------------------------------------------------------

    def _get_columns_for_categories(self, category):

        # the web interface has switched to a different category and needs category headers

        from warpseq.model.pattern import PERCUSSION, STANDARD

        if category == CATEGORY_COMMON:
            if self.for_transform:
                return []
            elif self.pattern_type == PERCUSSION:
                return DRUM_COMMON
            else:
                return INST_COMMON
        elif category == CATEGORY_PITCH:
            if self.for_transform:
                return TRANSFORM_PITCH
            elif self.pattern_type == PERCUSSION:
                return DRUM_PITCH
            else:
                return INST_PITCH
        elif category == CATEGORY_TIME:
            return TIME
        elif category == CATEGORY_MOD:
            return MODULATION
        elif category == CATEGORY_CONTROL:
            return CONTROL
        elif category == CATEGORY_VARIABLES:
            return VARIABLES
        else:
            raise Exception("unknown category")

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

            # ccs - convert four key/pair columns to a single dict
            k1 = x.get("cc_a", None)
            v1 = x.get("cc_a_value", None)
            k2 = x.get("cc_b", None)
            v2 = x.get("cc_b_value", None)
            k3 = x.get("cc_c", None)
            v3 = x.get("cc_c_value", None)
            k4 = x.get("cc_d", None)
            v4 = x.get("cc_d_value", None)
            ccs = dict()
            if k1 is not None:
                k1 = safe_int(k1)
            if k2 is not None:
                k2 = safe_int(k2)
            if k3 is not None:
                k3 = safe_int(k3)
            if k4 is not None:
                k4 = safe_int(k4)
            if k1:
                ccs[str(k1)] = v1
            if k2:
                ccs[str(k2)] = v2
            if k3:
                ccs[str(k3)] = v3
            if k4:
                ccs[str(k4)] = v4
            x["ccs"] = ccs

            # variables - convert four key/pair columns to a single dict
            # TODO: move  with above into a helper function


            k1 = x.get("v_a", None)
            v1 = x.get("v_a_value", None)
            k2 = x.get("v_b", None)
            v2 = x.get("v_b_value", None)
            k3 = x.get("v_c", None)
            v3 = x.get("v_c_value", None)
            k4 = x.get("v_d", None)
            v4 = x.get("v_d_value", None)
            variables = dict()
            if k1:
                variables[str(k1)] = v1
            if k2:
                variables[str(k2)] = v2
            if k3:
                variables[str(k3)] = v3
            if k4:
                variables[str(k4)] = v4

            x["variables"] = variables

        for (i,x) in enumerate(web_slots):
            slot = Slot()

            for (k,v) in x.items():

                results2 = self.parse_field(i, k, v, errors)
                if not results2:
                    # this can happen with fields like 'cc_a_value' which are not really fields on the object
                    continue

                (ok, new_value) = results2

                if ok:
                    setattr(slot, k, new_value)

            results.append(slot)

        if len(errors):
            return (False, results, errors)
        else:
            return (True, self.fixup_slots(results), errors)

    # ------------------------------------------------------------------------------------------------------------------

    def fixup_slots(self, slots):
        for x in slots:

            if self.pattern_type == 'standard':
                x.note = None
                x.octave = None
                x.D1 = None
                x.D2 = None
                x.D3 = None
                x.D4 = None
                x.D5 = None
                x.D6 = None
                x.D7 = None
                x.D8 = None
                if not x.degree and not x.track_grab:
                     x.rest = True

            elif self.pattern_type == 'percussion':
                x.degree = None
                if not (x.D1 or x.D2 or x.D3 or x.D4 or x.D5 or x.D6 or x.D7 or x.D8):
                    x.rest = True

        return slots

    # ------------------------------------------------------------------------------------------------------------------

    def parse_field(self, row, key, value, errors, force=None):

        svalue = str(value).strip()


        if (not force) and (key in DICT_COLUMNS):
            detail = {}
            is_ok = True
            for (k,v) in value.items():
                if key == 'variables':
                    (ok, value) = self.parse_field(row, key, v, errors, force='str')
                    if not ok:
                        return (False, None)
                elif key == 'ccs':
                    (ok, value) = self.parse_field(row, key, v, errors, force='int')
                    if not ok:
                        return (False, None)
                detail[str(k)] = value
            return (is_ok, detail)

        if "," in svalue:
            choices = value.split(",")
            temp_results = [ self.parse_field(row, key, x, errors, force=force) for x in choices ]
            status = [ x[0] for x in temp_results ]
            values = [ x[1] for x in temp_results ]
            if False in status:
                return (False, None)
            else:
                return (True, RandomChoice(*values))

        if ":" in svalue and ((key in INT_COLUMNS or key in FLOAT_COLUMNS) or force):
            tokens = value.split(':')
            (left, right) = (tokens[0], tokens[1:])
            right = ":".join(right)
            (left_status, left_value) = self.parse_field(row, key, left, errors, force=force)
            if not left_status:
                return (False, None)
            (right_status, right_value) = self.parse_field(row, key, right, errors, force=force)
            if not right_status:
                return (False, None)
            return (True, RandomRange(left_value, right_value))

        if svalue.startswith("@"):
            return (True, DataGrab(value[1:]))

        if svalue.startswith("$"):
            return (True, LoadVariable(value[1:]))

        if key in INT_COLUMNS or force == 'int':
            return self._parse_int_field(row, key, value, errors)
        elif key in BOOL_COLUMNS:
            return self._parse_bool_field(row, key, value, errors)
        elif key in STR_COLUMNS or force == 'str':
            return self._parse_str_field(row, key, value, errors)
        elif key in FLOAT_COLUMNS:
            return self._parse_float_field(row, key, value, errors)

        else:
            # probably one of the MIDI CC values, this is ok.
            # raise Exception("unknown key: %s" % key)
            pass

    # ------------------------------------------------------------------------------------------------------------------

    def _parse_int_field(self, row, key, value, errors):

        if str(value).strip() in [ '', 'None' ]:
            return (True, None)

        try:
            x = int(value)
            return (True, x)
        except ValueError:
            errors.append(dict(row=row, key=key, value=value, reason="cannot parse as integer"))
            return (False, None)

    def _parse_bool_field(self, row, key, value, errors):

        sv = str(value).strip().lower()

        if sv in [ '', 'none' ]:
            return (True, False)

        if sv in [ "false", "f", "0", "n", "no" ]:
            return (True, False)
        elif sv in [ "true", "t", "1", "y", "yes" ]:
            return (True, True)
        try:
            x = float(value)
            return (True, Probability(x,True,False))
        except ValueError:
            errors.append(dict(row=row, key=key, value=value, reason="cannot parse as bool or float"))
            return (False, None)

    def _parse_str_field(self, row, key, value, errors):

        from warpseq.model.chord import CHORD_TYPE_KEYS
        from warpseq.model.note import NOTES

        if str(value).strip() in [ '', 'None' ]:
            return (True, None)

        if key == 'chord_type':
            if str(value) not in CHORD_TYPE_KEYS:
                errors.append(dict(row=row, key=key, value=value, reason="is not a known chord type"))
                return (False, None)

        if key == 'note':
            if str(value).upper() not in NOTES:
                errors.append(dict(row=row, key=key, value=value, reason="is not a known note name"))
                return (False, None)

        return (True, str(value))

    def _parse_float_field(self, row, key, value, errors):

        if str(value).strip() in [ '', 'None' ]:
            return (True, None)

        try:
            x = float(value)
            return (True, x)
        except ValueError:
            errors.append(dict(row=row, key=key, value=value, reason="cannot parse as float"))
            return (False, None)




