""" ``comp`` module.
"""

import sys

PY_MAJOR = sys.version_info[0]
PY_MINOR = sys.version_info[1]
PY2 = PY_MAJOR == 2
PY3 = PY_MAJOR >= 3


if PY3:  # pragma: nocover
    from io import BytesIO
    from queue import LifoQueue, Queue

    xrange = range
    str_type = str
else:  # pragma: nocover
    from Queue import Queue  # noqa
    from cStringIO import StringIO as BytesIO  # noqa

    try:
        from Queue import LifoQueue  # noqa
    except ImportError:

        class LifoQueue(Queue):  # noqa
            def _init(self, maxsize):
                self.queue = []
                self.maxsize = maxsize

            def _qsize(self, len=len):
                return len(self.queue)

            def _put(self, item):
                self.queue.append(item)

            def _get(self):
                return self.queue.pop()

    xrange = range
    xrange = xrange
    str_type = unicode  # noqa: F821


if PY3:  # pragma: nocover

    def ntob(n, encoding):
        """Converts native string to bytes"""
        return n.encode(encoding)

    def bton(b, encoding):
        """Converts bytes to native string"""
        return b.decode(encoding)

    def u(s):
        return s


else:  # pragma: nocover

    def ntob(n, encoding):  # noqa
        """Converts native string to bytes"""
        return n

    def bton(b, encoding):  # noqa
        """Converts bytes to native string"""
        return b

    def u(s):
        return unicode(s, "unicode_escape")  # noqa: F821


if PY2 and PY_MINOR == 4:  # pragma: nocover
    __import__ = __import__
else:  # pragma: nocover
    # perform absolute import
    __saved_import__ = __import__

    def __import__(name, globals=None, locals=None, f=None):  # noqa: N807
        return __saved_import__(name, globals, locals, f, 0)


try:  # noqa pragma: nocover
    # from collections import defaultdict
    defaultdict = __import__(
        "collections", None, None, ["defaultdict"]
    ).defaultdict
except AttributeError:  # pragma: nocover

    class defaultdict(dict):  # noqa: N801
        def __init__(self, default_factory=None, *args, **kwargs):
            if default_factory and not callable(default_factory):
                raise TypeError("first argument must be callable")
            super(defaultdict, self).__init__(*args, **kwargs)
            self.default_factory = default_factory

        def __getitem__(self, key):
            try:
                return dict.__getitem__(self, key)
            except KeyError:
                return self.__missing__(key)

        def __missing__(self, key):
            if self.default_factory is None:
                raise KeyError(key)
            self[key] = value = self.default_factory()
            return value

        def __reduce__(self):
            if self.default_factory is None:
                args = tuple()
            else:
                args = (self.default_factory,)
            return type(self), args, None, None, self.items()

        def __repr__(self):
            return "defaultdict(%s, %s)" % (
                self.default_factory,
                dict.__repr__(self),
            )


try:  # pragma: nocover
    from email.utils import parsedate
except ImportError:  # pragma: nocover
    import time

    def parsedate(s):  # noqa
        return time.strptime(s, "%a, %d %b %Y %H:%M:%S GMT")


if PY3:  # pragma: nocover
    from http.cookies import SimpleCookie
else:  # pragma: nocover
    from Cookie import SimpleCookie  # noqa

if PY3:  # pragma: nocover
    from http.client import HTTPConnection, HTTPSConnection
    from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit
else:  # pragma: nocover
    from urllib import urlencode  # noqa

    from httplib import HTTPConnection  # noqa
    from httplib import HTTPSConnection  # noqa
    from urlparse import urljoin  # noqa
    from urlparse import urlsplit  # noqa
    from urlparse import urlunsplit  # noqa

if PY3:  # pragma: nocover

    def ref_gettext(t):
        return t.gettext


else:  # pragma: nocover

    def ref_gettext(t):  # noqa
        return t.ugettext


if PY3 or PY2 and PY_MINOR >= 6:  # pragma: nocover
    m = __import__("json", None, None, ["JSONEncoder", "dumps", "loads"])
    SimpleJSONEncoder = m.JSONEncoder
    json_dumps = m.dumps
    json_loads = m.loads
    del m
else:  # pragma: nocover
    try:
        from simplejson import (  # noqa
            JSONEncoder as SimpleJSONEncoder,
            dumps,
            loads as json_loads,
        )

        def json_dumps(obj, **kw):  # noqa
            return dumps(obj, use_decimal=False, **kw)

    except ImportError:
        SimpleJSONEncoder = object  # noqa

        def json_dumps(obj, **kw):  # noqa
            raise NotImplementedError("JSON encoder is required.")

        def json_loads(s, **kw):  # noqa
            raise NotImplementedError("JSON decoder is required.")


if PY3 and PY_MINOR >= 3:  # pragma: nocover
    from decimal import Decimal
else:  # pragma: nocover
    try:
        from cdecimal import Decimal  # noqa
    except ImportError:
        from decimal import Decimal  # noqa

GzipFile = __import__("gzip", None, None, ["GzipFile"]).GzipFile

if PY2 and PY_MINOR < 7:  # pragma: nocover
    __saved_gzipfile__ = GzipFile

    def GzipFile(  # noqa: N802
        filename=None,
        mode=None,
        compresslevel=9,
        fileobj=None,
        mtime=None,
    ):
        return __saved_gzipfile__(filename, mode, compresslevel, fileobj)
