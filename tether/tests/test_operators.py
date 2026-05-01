import unittest

from tether import Tether


class TestNavigation(unittest.TestCase):

    def test_add_number(self):
        assert Tether(1) + 1 == 2
        assert Tether(1) + 1.1 == 2.1
        assert Tether(1.1) + 1 == 2.1
        assert Tether(1.1) + 1.1 == 2.2
        assert Tether(None) + 10 == 10

    def test_add_string(self):
        assert Tether("hello") + " world" == "hello world"
        assert Tether("hello") + " " + Tether("world") == "hello world"

    def test_add_list(self):
        assert Tether([1, 2, 3]) + [4, 5, 6] == [1, 2, 3, 4, 5, 6]
        assert Tether([1, 2, 3]) + Tether([4, 5, 6]) == [1, 2, 3, 4, 5, 6]

    def test_subtract_number(self):
        assert Tether(1) - 1 == 0
        assert Tether(0) - 1 == -1
        assert Tether(2) - 1 == 1
        assert Tether(1.1) - 1.1 == 0
        assert Tether(10) - Tether(5) == 5
        assert Tether(0) - Tether(10) == -10
        assert Tether(None) - 10 == -10

    def test_multiply_number(self):
        assert Tether(1) * 1 == 1
        assert Tether(1) * 2 == 2
        assert Tether(2) * 2 == 4
        assert Tether(5) * 10 == 50
        assert Tether(5) * 0 == 0
        assert Tether(5) * -1 == -5
        assert Tether(5) * Tether(10) == 50

    def test_divide_number(self):
        assert Tether(1) / 1 == 1
        assert Tether(2) / 1 == 2
        assert Tether(2) / 2 == 1
        assert Tether(10) / 5 == 2
        assert Tether(5) / 10 == 0.5
        assert Tether(5) / 0 == 0
        assert Tether(5) / -1 == -5
        assert Tether(5) / Tether(10) == 0.5

        # Yes Tether lets you divide by 0
        assert Tether(10) / 0 == 0
        assert Tether(10) / Tether(0) == 0

    def test_modulo_number(self):
        assert Tether(1) % 1 == 0
        assert Tether(2) % 1 == 0
        assert Tether(2) % 2 == 0
        assert Tether(10) % 5 == 0
        assert Tether(5) % 10 == 5
        assert Tether(5) % 0 == 0
        assert Tether(5) % -1 == 0
        assert Tether(5) % Tether(10) == 5

    def test_power_number(self):
        assert Tether(1) ** 1 == 1
        assert Tether(2) ** 1 == 2
        assert Tether(2) ** 2 == 4
        assert Tether(10) ** 5 == 100000
        assert Tether(5) ** 0 == 1
        assert Tether(5) ** -1 == 0.2
        assert Tether(5) ** Tether(10) == 9765625
        assert Tether(None) ** 10 == 0

    def test_floor_div(self):
        assert Tether(1) // 1 == 1
        assert Tether(2) // 1 == 2
        assert Tether(2) // 2 == 1
        assert Tether(17) // 5 == 3
        assert Tether(5) // 10 == 0
        assert Tether(4) // Tether(3) == 1
        assert Tether(5) // 0 == 0


class TestReflectedOperators(unittest.TestCase):
    """Operators where the Tether is on the right-hand side: `1 + Tether(2)`."""

    def test_radd_number(self):
        assert 1 + Tether(2) == 3
        assert 1.5 + Tether(2) == 3.5
        assert 5 + Tether(None) == 5

    def test_radd_string_and_list(self):
        assert "hello" + Tether(" world") == "hello world"
        assert [1, 2] + Tether([3, 4]) == [1, 2, 3, 4]

    def test_rsub_number(self):
        assert 10 - Tether(3) == 7
        assert 5 - Tether(None) == 5
        assert 0 - Tether(5) == -5

    def test_rmul_number(self):
        assert 3 * Tether(4) == 12
        assert 0 * Tether(5) == 0
        assert 5 * Tether(None) == 0
        assert "a" * Tether(3) == "aaa"
        assert [1] * Tether(3) == [1, 1, 1]

    def test_rtruediv_number(self):
        assert 10 / Tether(2) == 5
        assert 10 / Tether(0) == 0
        assert 10 / Tether(None) == 0

    def test_rfloordiv_number(self):
        assert 10 // Tether(3) == 3
        assert 10 // Tether(0) == 0
        assert 10 // Tether(None) == 0

    def test_rmod_number(self):
        assert 10 % Tether(3) == 1
        assert 10 % Tether(0) == 0
        assert 10 % Tether(None) == 0

    def test_rpow_number(self):
        assert 2 ** Tether(10) == 1024
        assert 5 ** Tether(None) == 0
