from collections.abc import Iterable, Mapping


def isdictlike(obj):
    return isinstance(obj, Mapping) or hasattr(obj, "items")


def islistlike(obj):
    return isiterable(obj) and not isdictlike(obj) and not isinstance(obj, str)


def isiterable(obj):
    return isinstance(obj, Iterable)


def isnestable(obj):
    return isdictlike(obj) or islistlike(obj)
