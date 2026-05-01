import unittest

from tether import Tether


class TestBuiltins(unittest.TestCase):

    def test_repr(self):
        assert repr(Tether(1)) == "1"
        assert repr(Tether("hello")) == "'hello'"
        assert repr(Tether([1, 2, 3])) == "[1, 2, 3]"
        assert repr(Tether({"a": 1, "b": 2})) == "{'a': 1, 'b': 2}"

    def test_str(self):
        assert str(Tether(1)) == "1"
        assert str(Tether("hello")) == "hello"
        assert str(Tether([1, 2, 3])) == "[1, 2, 3]"
        assert str(Tether({"a": 1, "b": 2})) == "{'a': 1, 'b': 2}"
        assert str(Tether(None)) == "None"

    def test_hash(self):
        assert hash(Tether(None)) == hash(None)
        assert hash(Tether(1)) == hash(1)
        assert hash(Tether("hello")) == hash("hello")

    def test_slots_no_instance_dict(self):
        # Tether uses __slots__ to keep the wrapper itself shallow — verify
        # there's no per-instance __dict__ and arbitrary attrs can't be set.
        c = Tether(1)
        self.assertFalse(hasattr(type(c), "__dict__") and "__dict__" in type(c).__dict__)
        with self.assertRaises(AttributeError):
            c.arbitrary_attr = "should not be settable"

    def test_pickle_round_trip(self):
        import pickle

        original = Tether({"a": 1, "b": [2, 3]})
        restored = pickle.loads(pickle.dumps(original))
        assert restored == {"a": 1, "b": [2, 3]}


class TestNumericCoercion(unittest.TestCase):
    def test_int(self):
        assert int(Tether(5)) == 5
        assert int(Tether(5.7)) == 5
        assert int(Tether("5")) == 5
        assert int(Tether(None)) == 0

    def test_float(self):
        assert float(Tether(5)) == 5.0
        assert float(Tether(5.5)) == 5.5
        assert float(Tether("5.5")) == 5.5
        assert float(Tether(None)) == 0.0

    def test_index_for_list_subscripting(self):
        # __index__ is what makes `[1,2,3][Tether(0)]` work.
        data = [10, 20, 30]
        assert data[Tether(0)] == 10
        assert data[Tether(2)] == 30
        # None is treated as 0 for consistency with arithmetic.
        assert data[Tether(None)] == 10

    def test_index_for_range(self):
        assert list(range(Tether(3))) == [0, 1, 2]
        assert list(range(Tether(None))) == []
