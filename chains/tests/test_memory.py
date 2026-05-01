import gc
import sys
import tracemalloc
import unittest

from chains import Chain


class TestMemory(unittest.TestCase):
    def test_wrapped_object_is_referenced_not_copied(self):
        # The wrapper holds a reference to the original object, not a copy —
        # wrapping a 100MB dict should not double memory usage.
        original = {"a": [1, 2, 3], "b": {"nested": "value"}}
        wrapper = Chain(original)
        assert wrapper._wrapped is original
        # Inner object identity is also preserved through navigation.
        assert wrapper.a._wrapped is original["a"]
        assert wrapper.b._wrapped is original["b"]

    def test_instance_size_is_bounded(self):
        # __slots__ keeps each Chain wrapper to a small fixed size (~40 bytes
        # on CPython 3.13). Without slots a per-instance __dict__ pushed it
        # past 300 bytes. Allow generous headroom for other interpreters.
        size = sys.getsizeof(Chain(None))
        assert size < 100, f"Chain instance is {size} bytes; expected <100"

    def test_no_per_instance_dict(self):
        # Slot-only classes have no __dict__ on instances.
        c = Chain(1)
        assert not hasattr(c, "__dict__")

    def test_arbitrary_attributes_cannot_be_set(self):
        # Slots also prevent surprise attribute creation.
        c = Chain(1)
        with self.assertRaises(AttributeError):
            c.unexpected = "value"

    def test_wrapping_large_dict_uses_constant_memory(self):
        # The 100k-entry dict itself occupies several MB. Wrapping should
        # only add a tiny constant overhead (the Chain wrapper plus
        # tracemalloc bookkeeping), proving no proportional copy of the data.
        big = {f"k{i}": i for i in range(100_000)}
        gc.collect()
        tracemalloc.start()
        baseline = tracemalloc.take_snapshot()
        wrapper = Chain(big)
        after = tracemalloc.take_snapshot()
        delta = sum(d.size_diff for d in after.compare_to(baseline, "lineno"))
        tracemalloc.stop()
        self.assertLess(delta, 10_000)
        assert wrapper._wrapped is big
