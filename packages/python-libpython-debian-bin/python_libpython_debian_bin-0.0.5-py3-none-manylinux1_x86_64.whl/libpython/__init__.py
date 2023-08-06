def init_libpython():
    import ctypes
    import pkg_resources
    import six
    if six.PY2:
        t = pkg_resources.resource_filename(__name__, "libpython2.7.so.1.0")
    else:
        t = pkg_resources.resource_filename(__name__, "libpython3.6m.so.1.0")
        ctypes.CDLL(t)
        t = pkg_resources.resource_filename(__name__, "libpython3.6m.a")

    ctypes.CDLL(t)
