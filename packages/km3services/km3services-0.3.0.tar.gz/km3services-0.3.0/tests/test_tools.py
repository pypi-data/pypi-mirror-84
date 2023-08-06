#!/usr/bin/env python3
import unittest

from km3services._tools import _infinite, _zipequalize


def test_infinite():
    a = 1
    infinite_a = _infinite(a)
    for n in [1, 5, 100]:
        assert n == len(list(zip(range(n), _infinite(a))))


class TestZipEqualise(unittest.TestCase):
    def test_zipequalize(self):
        assert 1 == len(list(zip(*_zipequalize([1], [1]))))
        assert 3 == len(list(zip(*_zipequalize([1], [1, 2, 3]))))
        assert 3 == len(list(zip(*_zipequalize([1], [1, 2, 3], [4]))))

        a, b, c = list(zip(*_zipequalize([1], [1, 2, 3])))
        self.assertTupleEqual(a, (1, 1))
        self.assertTupleEqual(b, (1, 2))
        self.assertTupleEqual(c, (1, 3))

    def test_zipequalize_raises_if_dim_mismatch(self):
        with self.assertRaises(ValueError) as e:
            assert 3 == len(list(zip(*_zipequalize([1, 2], [1, 2, 3]))))
