import unittest

from chains import Chain


class TestBuiltins(unittest.TestCase):

    def test_repr(self):
        assert repr(Chain(1)) == "1"
        assert repr(Chain("hello")) == "'hello'"
        assert repr(Chain([1, 2, 3])) == "[1, 2, 3]"
        assert repr(Chain({"a": 1, "b": 2})) == "{'a': 1, 'b': 2}"

    def test_str(self):
        assert str(Chain(1)) == "1"
        assert str(Chain("hello")) == "hello"
        assert str(Chain([1, 2, 3])) == "[1, 2, 3]"
        assert str(Chain({"a": 1, "b": 2})) == "{'a': 1, 'b': 2}"
        assert str(Chain(None)) == "None"

    def test_hash(self):
        assert hash(Chain(None)) == hash(None)
        assert hash(Chain(1)) == hash(1)
        assert hash(Chain("hello")) == hash("hello")

    def test_slots_no_instance_dict(self):
        # Chain uses __slots__ to keep the wrapper itself shallow — verify
        # there's no per-instance __dict__ and arbitrary attrs can't be set.
        c = Chain(1)
        self.assertFalse(hasattr(type(c), "__dict__") and "__dict__" in type(c).__dict__)
        with self.assertRaises(AttributeError):
            c.arbitrary_attr = "should not be settable"

    def test_pickle_round_trip(self):
        import pickle

        original = Chain({"a": 1, "b": [2, 3]})
        restored = pickle.loads(pickle.dumps(original))
        assert restored == {"a": 1, "b": [2, 3]}


class TestNumericCoercion(unittest.TestCase):
    def test_int(self):
        assert int(Chain(5)) == 5
        assert int(Chain(5.7)) == 5
        assert int(Chain("5")) == 5
        assert int(Chain(None)) == 0

    def test_float(self):
        assert float(Chain(5)) == 5.0
        assert float(Chain(5.5)) == 5.5
        assert float(Chain("5.5")) == 5.5
        assert float(Chain(None)) == 0.0

    def test_index_for_list_subscripting(self):
        # __index__ is what makes `[1,2,3][Chain(0)]` work.
        data = [10, 20, 30]
        assert data[Chain(0)] == 10
        assert data[Chain(2)] == 30
        # None is treated as 0 for consistency with arithmetic.
        assert data[Chain(None)] == 10

    def test_index_for_range(self):
        assert list(range(Chain(3))) == [0, 1, 2]
        assert list(range(Chain(None))) == []
