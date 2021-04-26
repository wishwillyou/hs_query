from datetime import datetime, date

from bson import ObjectId

HS_CODE_DB = 'hs_code'


class FieldNotLoadedError(object):
    pass


class MongoMixin(object):
    @classmethod
    def all_fields(cls):
        return cls._fields.keys()

    def dict_include(self):
        return self.all_fields()

    def dict_exclude(self):
        return []

    # Default to_dict, can be overridden
    # Returns all fields, with values transformed:
    # -ObjectIds casted to strings
    # -Date/Datetime formatted as string, with format specified by
    # default_date_format property of class
    # -Values of lists and dicts recursively transformed
    def to_dict_default(self, date_format="%Y-%m-%d", ignore_unloaded=False):
        def transform_field(value):
            if isinstance(value, ObjectId):
                return str(value)
            elif isinstance(value, list):
                return map(transform_field, value)
            elif issubclass(value.__class__, MongoMixin):
                return value.to_dict() if hasattr(value, 'to_dict') else \
                    value.to_dict_default(ignore_unloaded=ignore_unloaded)
            elif isinstance(value, dict):
                return dict([(key, transform_field(val))
                             for key, val in value.iteritems()])
            elif isinstance(value, (datetime, date)):
                return value.strftime(date_format)
            return value

        _dict = {}
        exclude = self.dict_exclude()
        for fname in self.dict_include():
            if fname not in exclude:
                try:
                    value = getattr(self, fname)
                except FieldNotLoadedError:
                    # In case fields was specified,
                    # some fields may not be loaded,
                    # so just skip from unloaded fields
                    if not ignore_unloaded:
                        raise
                else:
                    _dict[fname] = transform_field(value)
        return _dict
