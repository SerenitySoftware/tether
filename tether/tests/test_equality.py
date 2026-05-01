from decimal import Decimal
import unittest

from tether import Tether


class TestEquality(unittest.TestCase):

    def test_none(self):
        wrapped_none = Tether(None)
        assert wrapped_none == None
        assert wrapped_none() is None
        assert wrapped_none != ""

        wrapped_empty = Tether("")
        assert wrapped_empty != None
        assert wrapped_empty() == ""
        assert wrapped_empty is not None

    def test_booleans(self):
        wrapped_true = Tether(True)
        wrapped_nested_true = Tether({"nested": True}).nested
        wrapped_false = Tether(False)
        wrapped_nested_false = Tether({"nested": False}).nested

        assert wrapped_true == True
        assert wrapped_true != False
        assert wrapped_true() is True
        assert wrapped_true() is not False

        assert wrapped_false == False
        assert wrapped_false != True
        assert wrapped_false() is False
        assert wrapped_false() is not True

        assert wrapped_nested_true == True
        assert wrapped_nested_true != False
        assert wrapped_nested_true() is True
        assert wrapped_nested_true() is not False

        assert wrapped_nested_false == False
        assert wrapped_nested_false != True
        assert wrapped_nested_false() is False
        assert wrapped_nested_false() is not True

    def test_strings(self):
        assert Tether("") == ""
        assert Tether("hello") == "hello"
        assert Tether("hello") != "world"

    def test_raw_number_equality(self):
        assert Tether(0) == 0
        assert Tether(1) == 1
        assert Tether(-1) == -1
        assert Tether(1.1) == 1.1
        assert Tether(-1.1) == -1.1

    def test_raw_number_inequality(self):
        assert Tether(1) != 0
        assert Tether(1) != 1.1
        assert Tether(1) != -1
        assert Tether(1) != -1.1
        assert Tether(1.1) != 0
        assert Tether(1.1) != 1
        assert Tether(1.1) != -1
        assert Tether(1.1) != -1.1
        assert Tether(-1) != 0
        assert Tether(-1) != 1
        assert Tether(-1) != 1.1
        assert Tether(-1) != -1.1
        assert Tether(-1.1) != 0
        assert Tether(-1.1) != 1
        assert Tether(-1.1) != 1.1
        assert Tether(-1.1) != -1

    def test_raw_number_greater_than(self):
        assert Tether(1) > 0
        assert Tether(1) > -1
        assert Tether(1) > 0.5
        assert Tether(1) > -0.5

        assert Tether(1) >= 1
        assert Tether(1) >= 0
        assert Tether(1) >= -1
        assert Tether(1) >= 0.5

        self.assertTrue(1 > Tether({"numeric": 5}).garbage)
        self.assertTrue(1 >= Tether({"numeric": 5}).garbage)

        self.assertFalse(Tether(None) > 1)
        self.assertFalse(Tether(None) >= 1)

    def test_raw_number_less_than(self):
        assert Tether(1) < 2
        assert Tether(1) < 1.1
        assert Tether(1) < 1.5
        assert Tether(-1) < 0

        assert Tether(1) <= 2
        assert Tether(1) <= 1.1
        assert Tether(1) <= 1
        assert Tether(-1) <= 0

        self.assertFalse(Tether({"numeric": 5}).garbage < 0)
        self.assertTrue(Tether({"numeric": 5}).garbage <= 0)
        self.assertTrue(Tether({"numeric": 5}).garbage < 1)
        self.assertTrue(Tether({"numeric": 5}).garbage <= 1)

        self.assertTrue(Tether(None) < 1)
        self.assertTrue(Tether(None) <= 1)

    def test_nested_numbers(self):
        assert Tether({"numeric": 5}).numeric == 5
        assert Tether({"numeric": 5}).numeric != 1
        assert Tether({"numeric": 5.5}).numeric == 5.5

    def test_floats(self):
        assert Tether(5.09245) == 5.09245
        assert Tether(5.09245) != 5.09246

    def test_decimals(self):
        assert Tether(Decimal("5.09245")) == Decimal("5.09245")
        assert Tether(Decimal("5.09245")) != Decimal("5.09246")

    def test_dicts(self):
        assert Tether({}) == {}
        assert Tether({"hello": "world"}) == {"hello": "world"}
        assert Tether({"foo": "bar"}) != {"baz": "qux"}
        assert Tether({"content": {"nested": "here"}}) == {"content": {"nested": "here"}}

    def test_lists(self):
        assert Tether([]) == []
        assert Tether([1, 2, 3]) == [1, 2, 3]
        assert Tether(["hello", "world"]) == ["hello", "world"]
        assert Tether([1, 2, 3]) != [3, 2, 1]
        assert Tether([1, 2, 3]) != [1, 2, 3, 4]
