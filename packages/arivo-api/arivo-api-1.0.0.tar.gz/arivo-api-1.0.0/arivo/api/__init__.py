import re
import threading

from .http import HttpBackend

timeout = 30

_locals = threading.local()


def _get_backend():
    backend = getattr(_locals, "backend", None)
    if not backend:
        backend = HttpBackend(timeout)
        setattr(_locals, "backend", backend)
    return backend


def camel_to_snake(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(string):
    return "".join([x.capitalize() for x in string.split("_")])


class Client:
    def __init__(self):
        self._keys = []

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            copy = self.__class__()
            snake_key = camel_to_snake(key)
            copy._keys = list(self._keys) + [snake_key]
            return copy

    def create(self, body=None):
        body = body or {}
        res = _get_backend().request("post", self._keys, body)
        return res

    def list(self, limit=None, offset=None, **filter):
        query_params = {**filter}
        if limit is not None:
            query_params["limit"] = limit
        if offset is not None:
            query_params["offset"] = offset
        res = _get_backend().request("get", self._keys, query_params=query_params)
        return res

    def read(self, id):
        res = _get_backend().request("get", self._keys + [str(id)])
        return res

    def update(self, id, body=None):
        body = body or {}
        res = _get_backend().request("put", self._keys + [str(id)], body)
        return res
