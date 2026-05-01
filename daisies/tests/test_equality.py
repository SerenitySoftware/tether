from decimal import Decimal
import unittest

from daisies import Chain


class TestEquality(unittest.TestCase):

    def test_none(self):
        wrapped_none = Chain(None)
        assert wrapped_none == None
        assert wrapped_none() is None
        assert wrapped_none != ""

        wrapped_empty = Chain("")
        assert wrapped_empty != None
        assert wrapped_empty() == ""
        assert wrapped_empty is not None

    def test_booleans(self):
        wrapped_true = Chain(True)
        wrapped_nested_true = Chain({"nested": True}).nested
        wrapped_false = Chain(False)
        wrapped_nested_false = Chain({"nested": False}).nested

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
        assert Chain("") == ""
        assert Chain("hello") == "hello"
        assert Chain("hello") != "world"

    def test_raw_number_equality(self):
        assert Chain(0) == 0
        assert Chain(1) == 1
        assert Chain(-1) == -1
        assert Chain(1.1) == 1.1
        assert Chain(-1.1) == -1.1

    def test_raw_number_inequality(self):
        assert Chain(1) != 0
        assert Chain(1) != 1.1
        assert Chain(1) != -1
        assert Chain(1) != -1.1
        assert Chain(1.1) != 0
        assert Chain(1.1) != 1
        assert Chain(1.1) != -1
        assert Chain(1.1) != -1.1
        assert Chain(-1) != 0
        assert Chain(-1) != 1
        assert Chain(-1) != 1.1
        assert Chain(-1) != -1.1
        assert Chain(-1.1) != 0
        assert Chain(-1.1) != 1
        assert Chain(-1.1) != 1.1
        assert Chain(-1.1) != -1

    def test_raw_number_greater_than(self):
        assert Chain(1) > 0
        assert Chain(1) > -1
        assert Chain(1) > 0.5
        assert Chain(1) > -0.5

        assert Chain(1) >= 1
        assert Chain(1) >= 0
        assert Chain(1) >= -1
        assert Chain(1) >= 0.5

        self.assertTrue(1 > Chain({"numeric": 5}).garbage)
        self.assertTrue(1 >= Chain({"numeric": 5}).garbage)

        self.assertFalse(Chain(None) > 1)
        self.assertFalse(Chain(None) >= 1)

    def test_raw_number_less_than(self):
        assert Chain(1) < 2
        assert Chain(1) < 1.1
        assert Chain(1) < 1.5
        assert Chain(-1) < 0

        assert Chain(1) <= 2
        assert Chain(1) <= 1.1
        assert Chain(1) <= 1
        assert Chain(-1) <= 0

        self.assertFalse(Chain({"numeric": 5}).garbage < 0)
        self.assertTrue(Chain({"numeric": 5}).garbage <= 0)
        self.assertTrue(Chain({"numeric": 5}).garbage < 1)
        self.assertTrue(Chain({"numeric": 5}).garbage <= 1)

        self.assertTrue(Chain(None) < 1)
        self.assertTrue(Chain(None) <= 1)

    def test_nested_numbers(self):
        assert Chain({"numeric": 5}).numeric == 5
        assert Chain({"numeric": 5}).numeric != 1
        assert Chain({"numeric": 5.5}).numeric == 5.5

    def test_floats(self):
        assert Chain(5.09245) == 5.09245
        assert Chain(5.09245) != 5.09246

    def test_decimals(self):
        assert Chain(Decimal("5.09245")) == Decimal("5.09245")
        assert Chain(Decimal("5.09245")) != Decimal("5.09246")

    def test_dicts(self):
        assert Chain({}) == {}
        assert Chain({"hello": "world"}) == {"hello": "world"}
        assert Chain({"foo": "bar"}) != {"baz": "qux"}
        assert Chain({"content": {"nested": "here"}}) == {"content": {"nested": "here"}}

    def test_lists(self):
        assert Chain([]) == []
        assert Chain([1, 2, 3]) == [1, 2, 3]
        assert Chain(["hello", "world"]) == ["hello", "world"]
        assert Chain([1, 2, 3]) != [3, 2, 1]
        assert Chain([1, 2, 3]) != [1, 2, 3, 4]
