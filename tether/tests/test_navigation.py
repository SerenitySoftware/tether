import unittest

from tether import Tether


class TestNavigation(unittest.TestCase):

    def test_raw_object(self):
        assert Tether(0) == 0
        assert Tether(False) == False
        assert Tether({"key": "value"}) == {"key": "value"}
        assert Tether([1, 2, 3]) == [1, 2, 3]

    def test_dict_access(self):
        assert Tether({"key": "value"}).key == "value"

    def test_dict_access_missing(self):
        assert Tether({"key": "value"}).missing() is None
        assert not Tether({"key": "value"}).missing

    def test_dict_access_nested(self):
        assert Tether({"nested": {"key": "value"}}).nested.key == "value"
        assert Tether({"nested": {"deeper": {"key": "value"}}}).nested.deeper == {"key": "value"}

    def test_dict_access_nested_missing(self):
        assert Tether({"nested": {"key": "value"}}).nested.missing() is None

    def test_list_access(self):
        assert Tether([1, 2, 3])[0] == 1
        assert Tether([1, 2, 3])[1] == 2
        assert Tether([1, 2, 3])[2] == 3

    def test_list_access_missing(self):
        assert Tether([1, 2, 3])[3]() is None

    def test_list_access_nested(self):
        assert Tether([{"key": "value"}])[0] == {"key": "value"}
        assert Tether({"items": [55, 8, 59]}).items[1] == 8
        assert Tether({"items": [{"hello": "world"}]}).items[0].hello == "world"

    def test_attribute_delegates_to_wrapped(self):
        assert Tether("hello").upper() == "HELLO"
        assert Tether("   hi   ").strip() == "hi"
        assert Tether([1, 2, 3]).index(2) == 1
        assert Tether({"name": "John"}).name.upper() == "JOHN"

    def test_attribute_missing_on_wrapped(self):
        assert Tether("hello").nonexistent() is None
        assert Tether([1, 2, 3]).does_not_exist() is None

    def test_attribute_on_none_wrapped(self):
        assert Tether(None).anything() is None
        assert Tether(None).deeply.nested.path() is None

    def test_dunder_attributes_not_delegated(self):
        # Dunder lookups should fall through to AttributeError so Python's
        # protocols (pickle, copy, repr, etc.) work correctly instead of
        # being intercepted into Tether(None) and recursing.
        with self.assertRaises(AttributeError):
            Tether({"a": 1}).__nonexistent_dunder__
