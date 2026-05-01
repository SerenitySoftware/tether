import unittest

from tether import Tether


class TestIterables(unittest.TestCase):
    def test_dict_keys(self):
        wrapped = Tether({"key": "value", "nested": {"key": "value"}})
        assert list(wrapped.keys()) == ["key", "nested"]
        assert list(wrapped.nested.keys()) == ["key"]
        assert "key" in wrapped.keys()
        assert "nested" in wrapped
        assert "missing" not in wrapped

    def test_lists(self):
        wrapped = Tether([1, 2, 3])
        assert wrapped[0] == 1
        assert wrapped[1] == 2
        assert wrapped[2] == 3
        assert 1 in wrapped
        assert 4 not in wrapped
        assert 1 in wrapped[0:2]

        assert sorted(wrapped, reverse=True) == [3, 2, 1]
        assert sorted(wrapped, reverse=False) == [1, 2, 3]
        assert sorted(wrapped[0:2], reverse=True) == [2, 1]
        assert sorted(wrapped[0:2], reverse=False) == [1, 2]

        for index, item in enumerate(wrapped):
            assert index + 1 == item

    def test_sets(self):
        assert Tether(set()) == set()
        assert Tether({1, 2, 3}) == {1, 2, 3}
        assert 1 in Tether({1, 2, 3})

    def test_strings(self):
        wrapped = Tether("abcdefghijklmnopqrstuvwxyz")
        assert wrapped[0] == "a"
        assert wrapped[1] == "b"
        assert wrapped[0:5] == "abcde"

        assert "a" in wrapped
        assert "z" in wrapped
        assert "abc" in wrapped
        assert "xyz" in wrapped

    def test_generators(self):
        wrapped = Tether(range(5))

        for index, item in enumerate(wrapped):
            assert index == item

    def test_non_iterable(self):
        with self.assertRaises(TypeError):
            enumerate(Tether(1))

    def test_no_contains(self):
        self.assertFalse("x" in Tether(None))

    def test_no_len(self):
        self.assertEqual(len(Tether(None)), 0)
