from .sniff import isdictlike, isiterable


class Chain:
    __slots__ = ("_wrapped",)

    def __init__(self, obj=None):
        self._wrapped = obj

    def __repr__(self):
        return repr(self._wrapped)

    def __call__(self, *args, **kwargs):
        if callable(self._wrapped):
            return self._wrapped(*args, **kwargs)

        return self._wrapped

    def __str__(self):
        return str(self._wrapped)

    def __hash__(self):
        return hash(self._wrapped)

    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        wrapped = self._wrapped

        if isdictlike(wrapped):
            attr = wrapped.get(name, None)
            if attr is None and name in ("keys", "items", "values") and hasattr(wrapped, name):
                attr = getattr(wrapped, name)
            return Chain(attr)

        if wrapped is None:
            return Chain(None)

        return Chain(getattr(wrapped, name, None))

    def __getitem__(self, key):
        item = None
        if self._wrapped and isiterable(self._wrapped):
            try:
                item = self._wrapped[key]
            except (KeyError, IndexError):
                pass

        return Chain(item)

    def __iter__(self):
        if isiterable(self._wrapped):
            return iter(self._wrapped)

        return None

    def __contains__(self, item):
        if self._wrapped is None:
            return False

        return item in self._wrapped

    def __len__(self):
        if not self._wrapped:
            return 0

        return len(self._wrapped)

    def __bool__(self):
        return bool(self._wrapped)

    def __eq__(self, other):
        return self._wrapped == self.__maybe_unwrap(other)

    def __ne__(self, other):
        return self._wrapped != self.__maybe_unwrap(other)

    def __gt__(self, other):
        comparison = self._wrapped
        if comparison is None:
            comparison = 0

        return comparison > other

    def __ge__(self, other):
        comparison = self._wrapped
        if comparison is None:
            comparison = 0

        return comparison >= other

    def __lt__(self, other):
        comparison = self._wrapped
        if comparison is None:
            comparison = 0

        return comparison < other

    def __le__(self, other):
        comparison = self._wrapped
        if comparison is None:
            comparison = 0

        return comparison <= other

    def __add__(self, other):
        if self._wrapped is None:
            return self.__maybe_wrap(other)

        return Chain(self._wrapped + self.__maybe_unwrap(other))

    def __sub__(self, other):
        if self._wrapped is None:
            return self.__maybe_wrap(-other)

        return Chain(self._wrapped - self.__maybe_unwrap(other))

    def __mul__(self, other):
        if self._wrapped is None or not other:
            return Chain(0)

        return Chain(self._wrapped * self.__maybe_unwrap(other))

    def __truediv__(self, other):
        if self._wrapped is None or not other:
            return Chain(0)

        return Chain(self._wrapped / self.__maybe_unwrap(other))

    def __floordiv__(self, other):
        if self._wrapped is None or not other:
            return Chain(0)

        return Chain(self._wrapped // self.__maybe_unwrap(other))

    def __mod__(self, other):
        if self._wrapped is None or not other:
            return Chain(0)

        return Chain(self._wrapped % self.__maybe_unwrap(other))

    def __pow__(self, other):
        if self._wrapped is None:
            return Chain(0)

        return Chain(self._wrapped ** self.__maybe_unwrap(other))

    def __radd__(self, other):
        if self._wrapped is None:
            return self.__maybe_wrap(other)

        return Chain(self.__maybe_unwrap(other) + self._wrapped)

    def __rsub__(self, other):
        if self._wrapped is None:
            return self.__maybe_wrap(other)

        return Chain(self.__maybe_unwrap(other) - self._wrapped)

    def __rmul__(self, other):
        if self._wrapped is None or not other:
            return Chain(0)

        return Chain(self.__maybe_unwrap(other) * self._wrapped)

    def __rtruediv__(self, other):
        if not self._wrapped:
            return Chain(0)

        return Chain(self.__maybe_unwrap(other) / self._wrapped)

    def __rfloordiv__(self, other):
        if not self._wrapped:
            return Chain(0)

        return Chain(self.__maybe_unwrap(other) // self._wrapped)

    def __rmod__(self, other):
        if not self._wrapped:
            return Chain(0)

        return Chain(self.__maybe_unwrap(other) % self._wrapped)

    def __rpow__(self, other):
        if self._wrapped is None:
            return Chain(0)

        return Chain(self.__maybe_unwrap(other) ** self._wrapped)

    def __int__(self):
        if self._wrapped is None:
            return 0

        return int(self._wrapped)

    def __float__(self):
        if self._wrapped is None:
            return 0.0

        return float(self._wrapped)

    def __index__(self):
        if self._wrapped is None:
            return 0

        return self._wrapped.__index__()

    @staticmethod
    def __maybe_wrap(obj):
        if not isinstance(obj, Chain):
            obj = Chain(obj)

        return obj

    @staticmethod
    def __maybe_unwrap(obj):
        if isinstance(obj, Chain):
            return obj._wrapped

        return obj
