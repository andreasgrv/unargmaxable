import json
import xxhash
import datetime
from flask import Response


def datetime_aware(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.strftime('%c')
    return o


def response(status, msg=None, **kwargs):
    d = dict(status=status,
             message=msg or '',
             **kwargs)
    json_response = json.dumps(d, default=datetime_aware)
    return Response(status=200,
                    response=json_response,
                    mimetype='application/json')


class Hasher:
    """Our hashing implementation. NOTE: if we change the hash algorithm we
    need to adapt on the front end as well."""
    def __init__(self, salt=None):
        super().__init__()
        self.salt = salt

    def __call__(self, **kwargs):
        """Returns hashed content.
        :kwargs: key value pairs, all content should be jsonisable.
        :returns: hex hash
        """
        content = json.dumps(kwargs)
        if self.salt is not None:
            content = '%s%s' % (content, self.salt)
        hs = xxhash.xxh64(content).hexdigest()
        return hs

    def hash_as_int(self, **kwargs):
        content = json.dumps(kwargs)
        if self.salt is not None:
            content = '%s%s' % (content, self.salt)
        hs = xxhash.xxh64(content).intdigest()
        return hs

    def hash_as_hex(self, **kwargs):
        content = json.dumps(kwargs)
        if self.salt is not None:
            content = '%s%s' % (content, self.salt)
        hs = xxhash.xxh64(content).hexdigest()
        return hs
