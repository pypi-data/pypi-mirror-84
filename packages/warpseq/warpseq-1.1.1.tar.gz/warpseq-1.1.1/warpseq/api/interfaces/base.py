# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net>
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.api.exceptions import *

class BaseApi(object):

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, public_api, song):

        self.api  = public_api
        self.song = song

        if self.__class__.add_method:
            self.fn_add         = getattr(self.song, self.__class__.add_method)

        self.add_required   = self.__class__.add_required
        self.edit_required  = self.__class__.edit_required

        if self.__class__.remove_method:
            self.fn_remove      = getattr(self.song, self.__class__.remove_method)

        self.public_fields = self.__class__.public_fields

    # ------------------------------------------------------------------------------------------------------------------

    def post_load(self):
        # called after any edit add/edit operation, for instance, to recompute a scale.
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def lookup(self, name=None, id=None, require=False, field=None):
        """
        See if an object with the given name is in the collection. If 'require' is True,
        raise an exception if it is not found, instead of returning None.
        """

        if name == "-" or (name is None and id is None):
            return None
        if id:
            id = str(id)

        coll = self._get_collection()

        if type(coll) == dict:

            for (k,v) in coll.items():
                if name and v.name == name:
                    return v
                elif id and v.obj_id == id:
                    return v

        else:

            for k in coll:
                if name and k.name == name:
                    return k
                elif id and k.obj_id == id:
                    return k

        if require:
            raise NotFound()

        return None

    # ------------------------------------------------------------------------------------------------------------------

    def list(self, show_hidden=True):
        """
        Return information about all objects in the collection.

        show_hidden=False can only be used with scene/track and is used to prevent temporary audition objects
        from being seen in the UI.
        """

        coll = self._get_collection()
        data = []
        if type(coll) == dict:
            for (k,v) in coll.items():
                data.append(self._short_details(v))
            return data
        else:
            if show_hidden is False:
                return [ self._short_details(x) for x in coll if not x.is_hidden() ]
            else:
                return [ self._short_details(x) for x in coll ]

    # ------------------------------------------------------------------------------------------------------------------

    def _short_details(self, obj):
        """
        Used by the list method to decide what information to return for each object in the collection.
        Usually just returns the name+ID except for Clip. Use .details() one object at a time for specifics.
        """
        return dict(name=obj.name, obj_id=obj.obj_id)

    # ------------------------------------------------------------------------------------------------------------------

    def details(self, name=None, id=None):
        """
        Returns all the public field information about the object, suitable for display in a web
        interface.
        """

        obj = self.lookup(name=name, id=id, require=True)
        data = obj.to_dict()
        new_data = dict()

        def nameify(obj):
            if hasattr(obj, 'obj_id'):
                return obj.name
            return obj

        for (k,v) in data.items():
            if k in self.public_fields:

                value = getattr(obj, k)

                if type(value) == list:

                    new_list = []

                    for entry in value:

                        if type(entry) in [ list, tuple ]:
                            new_list.append([ nameify(x) for x in entry ]) # value2.append([x.name for x in value ])
                        else:
                            new_list.append(nameify(entry))

                    value = new_list

                elif hasattr(value, 'obj_id'):
                    value = value.name

                new_data[k] = value

        self._update_details(new_data, obj)

        new_data['obj_id'] = obj.obj_id
        return new_data

    # ------------------------------------------------------------------------------------------------------------------

    def _update_details(self, details, obj):
        """
        Hook that allows a subclass to add or remove items before returning information in
        .details() to the caller.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------

    def _get_collection(self):
        """
        Pulls the object collection out of the song object.  The result could be a list or dict.
        """
        return getattr(self.song, self.__class__.song_collection)

    # ------------------------------------------------------------------------------------------------------------------

    def _require_input(self, what, params):
        """
        Verifies that certain required parameters are passed in.
        """
        for k in what:
            if params[k] is None:
                raise RequiredInput("%s is required" % k)

    # ------------------------------------------------------------------------------------------------------------------

    def _ok(self):
        """
        A placeholder for methods returning a consistent response when there is no information to return.
        Not really meaningful at this point.
        """
        # TODO: safe to eliminate
        return True

    # ------------------------------------------------------------------------------------------------------------------

    def _suggest_name(self):
        """
        Comes up with a name for new objects
        """
        basename = self.__class__.object_class.__name__

        if basename not in [ "Scene", "Track", "Instrument" ]:
            basename = basename[0].lower()
        else:
            basename = basename + " "

        for x in range(1,10000):
            name = "%s%s" % (basename, x)
            if not self.lookup(name):
                return name

        raise Exception("have you considered a career in quality assurance")

    # ------------------------------------------------------------------------------------------------------------------

    def _generic_new(self):

        name = self._suggest_name()
        obj = self.__class__.object_class(name=name)
        self.fn_add([obj])
        return obj.obj_id

    # ------------------------------------------------------------------------------------------------------------------

    def _generic_copy(self, id=None, name=None):

        from_obj = self.lookup(name=name, id=id, require=True)
        if not from_obj:
            raise NotFound()

        data = from_obj.to_dict()
        new_obj = self.__class__.object_class.from_dict(self.song, data)
        new_obj.name = self._suggest_copy_name(from_obj)
        new_obj.obj_id = new_obj.new_object_id()
        self.fn_add([new_obj])
        new_obj._additional_web_copy_steps(self.song, from_obj)
        return new_obj.obj_id

    # ------------------------------------------------------------------------------------------------------------------

    def _suggest_copy_name(self, obj):

        name = obj.name
        number = 0
        while True:
            number = number + 1
            try_name = "%s_%s" % (name, number)
            if self.lookup(name=try_name) is None:
                return try_name

    # ------------------------------------------------------------------------------------------------------------------

    def _generic_add(self, name, params):
        """
        Support code for adding new objects to a collection.
        """
        obj = self.lookup(name)
        del params['self']
        del params['name']
        self._require_input(self.add_required, params)
        if not obj:
            obj = self.__class__.object_class(name=name, **params)
            self.fn_add([obj])
            return self._ok()
        else:
            raise AlreadyExists()

    # ------------------------------------------------------------------------------------------------------------------

    def _generic_edit(self, name, params):
        """
        Support code for editing existing objects in a collection.
        """
        id = params.get('id', None)
        if id is None:
            obj = self.lookup(name)
        else:
            obj = self.lookup(id=id)
        if not obj:
            raise NotFound()
        del params["name"]
        del params["self"]

        self._require_input(self.edit_required, params)

        if "new_name" in params:
            value = params["new_name"]
            obj2 = self.lookup(value)
            if value and not obj2:
                # don't allow renaming to the name of an existing object
                obj.name = value
            del params["new_name"]



        for (k,v) in params.items():
            if k == 'id':
                continue
            if v is not None or k in self.__class__.nullable_edits:
                value = v
                setattr(obj, k, value)

        obj.post_load()

        return self._ok()

    # ------------------------------------------------------------------------------------------------------------------

    def _generic_remove(self, name):
        """
        Support code for removing objects from a collection.
        """
        obj = self.lookup(name, require=True)
        self.fn_remove(obj)
        return self._ok()

# ======================================================================================================================

class CollectionApi(BaseApi):

    def create(self):
        return self._generic_new()

    def copy(self, id=None, name=None):
        return self._generic_copy(id=id, name=name)

    def remove(self, name):
        return self._generic_remove(name)
