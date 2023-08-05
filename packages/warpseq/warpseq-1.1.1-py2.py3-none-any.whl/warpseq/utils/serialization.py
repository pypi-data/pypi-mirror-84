# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

import importlib

def save_relative_object(root, grand_parent, parent, obj, noref=False, key=None, depth=0):

    from warpseq.model.base import NewReferenceObject

    noref = False
    if obj == root:
        noref == True
    if obj is None:
        return obj
    elif type(obj) in [ str, float, int, bool]:
        return obj
    elif type(obj) in [ list, tuple ]:

        results = []
        for entry in obj:
            # deal with lists where they may be mixed nested elements (up to one level deep) - this occurs with transform storage inside clips.
            if type(entry) in [ list,  tuple ]:
                row = [ save_relative_object(root, grand_parent, parent, x, noref=noref, depth=depth + 1) for x in entry if not hasattr(x, 'is_hidden') or not x.is_hidden() ]
                results.append(row)
            else:
                if not hasattr(entry, 'is_hidden') or not entry.is_hidden():
                    row = save_relative_object(root, grand_parent, parent, entry, noref=noref, depth=depth+1)
                    results.append(row)
        return results

    elif type(obj) == dict:
        return { k: save_relative_object(root, grand_parent, parent, v, noref=noref, depth=depth+1) for (k,v) in obj.items() if not hasattr(v, 'is_hidden') or not v.is_hidden() }
    elif isinstance(obj, NewReferenceObject) and ((root == grand_parent) and (root != parent)):
        _cls = (obj.__class__.__module__, obj.__class__.__name__,)
        return dict(_ID=obj.obj_id, _CLS=_cls)
    elif isinstance(obj, object):
        results = dict()
        _cls = (obj.__class__.__module__, obj.__class__.__name__,)

        save_first = getattr(obj, '_SAVE_FIRST', [])
        save_second = [ x for x in obj.__slots__ if x not in save_first ]

        for k in save_first:
            if k.startswith("_"):
                continue
            value = getattr(obj, k)
            results[k] = save_relative_object(root, parent, obj, value, noref=noref, key=k, depth=depth+1)

        for k in save_second:
            if k.startswith("_"):
                continue
            value = getattr(obj, k)
            results[k] = save_relative_object(root, parent, obj, value, noref=noref, key=k, depth=depth+1)

        results['_CLS'] = _cls
        return results
    else:
        raise Exception("error")

def save_object(obj):
    result = save_relative_object(obj, obj, obj, obj, key=None, depth=0)
    return result

# ------------------------------------------------------------------------------------

def load_object(song, data):

    if data is None:
        return None

    if type(data) in [ int, float, bool, str ]:
        return data

    elif type(data) == list:
        res = [ load_object(song, x) for x in data ]
        return res

    elif '_ID' in data:
        method = getattr(song, "find_%s" % data['_CLS'][1].lower())
        res = method(data['_ID'])
        return res

    elif '_CLS' in data:
        (mod, classname) = data['_CLS']
        mod = importlib.import_module(mod)
        cls = getattr(mod, classname)
        del data['_CLS']
        params = { x : load_object(song, y) for (x,y) in data.items() }
        res = cls(**params)
        return res

    else:
        res = { k : load_object(song, v) for (k, v) in data.items() }
        return res
