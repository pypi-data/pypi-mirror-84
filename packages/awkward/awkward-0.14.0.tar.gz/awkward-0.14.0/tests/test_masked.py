#!/usr/bin/env python

# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-array/blob/master/LICENSE

import unittest

import numpy

from awkward import *

class Test(unittest.TestCase):
    def runTest(self):
        pass

    def test_masked_nbytes(self):
        assert isinstance(MaskedArray([True, False, True, False, True, False, True, False, True, False], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9], maskedwhen=True).nbytes, int)

    def test_masked_get(self):
        a = MaskedArray([True, False, True, False, True, False, True, False, True, False], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9], maskedwhen=True)
        assert a.tolist() == [None, 1.1, None, 3.3, None, 5.5, None, 7.7, None, 9.9]
        assert a[0] is None
        assert not a[1] is None
        assert a[5:].tolist() == [5.5, None, 7.7, None, 9.9]
        assert not a[5:][0] is None
        assert a[5:][1] is None
        assert a[[3, 2, 1]].tolist() == [3.3, None, 1.1]
        assert a[[True, True, True, True, True, False, False, False, False, False]].tolist() == [None, 1.1, None, 3.3, None]

    def test_masked_get_flip(self):
        a = MaskedArray([False, True, False, True, False, True, False, True, False, True], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9], maskedwhen=False)
        assert a.tolist() == [None, 1.1, None, 3.3, None, 5.5, None, 7.7, None, 9.9]
        assert a[0] is None
        assert not a[1] is None
        assert a[5:].tolist() == [5.5, None, 7.7, None, 9.9]
        assert not a[5:][0] is None
        assert a[5:][1] is None
        assert a[[3, 2, 1]].tolist() == [3.3, None, 1.1]
        assert a[[True, True, True, True, True, False, False, False, False, False]].tolist() == [None, 1.1, None, 3.3, None]

    def test_masked_ufunc(self):
        a = MaskedArray([True, False, True, False, True, False, True, False, True, False], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9], maskedwhen=True)
        b = MaskedArray([True, True, True, True, True, False, False, False, False, False], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9], maskedwhen=True)
        assert (a + b).tolist() == [None, None, None, None, None, 11.0, None, 15.4, None, 19.8]
        assert (a + [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]).tolist() == [None, 2.2, None, 6.6, None, 11.0, None, 15.4, None, 19.8]
        assert (a + numpy.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])).tolist() == [None, 2.2, None, 6.6, None, 11.0, None, 15.4, None, 19.8]
        assert (a + IndexedMaskedArray([-1, -1, -1, 1, -1, 2, -1, 4, -1, 3], [0.0, 1.1, 2.2, 3.3, 4.4])).tolist() == [None, None, None, 4.4, None, 7.7, None, 12.100000000000001, None, 13.2]

    def test_bitmasked_get(self):
        a = BitMaskedArray.fromboolmask([True, False, True, False, True, False, True, False, True, False], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9], maskedwhen=True, lsborder=True)
        assert a.tolist() == [None, 1.1, None, 3.3, None, 5.5, None, 7.7, None, 9.9]
        assert a[0] is None
        assert not a[1] is None
        assert a[5:].tolist() == [5.5, None, 7.7, None, 9.9]
        assert not a[5:][0] is None
        assert a[5:][1] is None
        assert a[[3, 2, 1]].tolist() == [3.3, None, 1.1]
        assert a[[True, True, True, True, True, False, False, False, False, False]].tolist() == [None, 1.1, None, 3.3, None]

        a = BitMaskedArray.fromboolmask([True, False, True, False, True, False, True, False, True, False], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9], maskedwhen=True, lsborder=False)
        assert a.tolist() == [None, 1.1, None, 3.3, None, 5.5, None, 7.7, None, 9.9]
        assert a[0] is None
        assert not a[1] is None
        assert a[5:].tolist() == [5.5, None, 7.7, None, 9.9]
        assert not a[5:][0] is None
        assert a[5:][1] is None
        assert a[[3, 2, 1]].tolist() == [3.3, None, 1.1]
        assert a[[True, True, True, True, True, False, False, False, False, False]].tolist() == [None, 1.1, None, 3.3, None]

    def test_bitmasked_get_flip(self):
        a = BitMaskedArray.fromboolmask([False, True, False, True, False, True, False, True, False, True], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9], maskedwhen=False, lsborder=True)
        assert a.tolist() == [None, 1.1, None, 3.3, None, 5.5, None, 7.7, None, 9.9]
        assert a[0] is None
        assert not a[1] is None
        assert a[5:].tolist() == [5.5, None, 7.7, None, 9.9]
        assert not a[5:][0] is None
        assert a[5:][1] is None
        assert a[[3, 2, 1]].tolist() == [3.3, None, 1.1]
        assert a[[True, True, True, True, True, False, False, False, False, False]].tolist() == [None, 1.1, None, 3.3, None]

        a = BitMaskedArray.fromboolmask([False, True, False, True, False, True, False, True, False, True], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9], maskedwhen=False, lsborder=False)
        assert a.tolist() == [None, 1.1, None, 3.3, None, 5.5, None, 7.7, None, 9.9]
        assert a[0] is None
        assert not a[1] is None
        assert a[5:].tolist() == [5.5, None, 7.7, None, 9.9]
        assert not a[5:][0] is None
        assert a[5:][1] is None
        assert a[[3, 2, 1]].tolist() == [3.3, None, 1.1]
        assert a[[True, True, True, True, True, False, False, False, False, False]].tolist() == [None, 1.1, None, 3.3, None]

    def test_bitmasked_arrow(self):
        # Apache Arrow layout example
        # https://github.com/apache/arrow/blob/master/format/Layout.md#null-bitmaps
        a = BitMaskedArray.fromboolmask([True, True, False, True, False, True], [0, 1, 999, 2, 999, 3], maskedwhen=False, lsborder=True)
        assert a.tolist() == [0, 1, None, 2, None, 3]

        # extra gunk at the end of the array
        a = BitMaskedArray.fromboolmask([True, True, False, True, False, True, True, True], [0, 1, 999, 2, 999, 3], maskedwhen=False, lsborder=True)
        assert a.tolist() == [0, 1, None, 2, None, 3]

        # opposite sign
        a = BitMaskedArray.fromboolmask([True, True, False, True, False, True, False, False], [0, 1, 999, 2, 999, 3], maskedwhen=False, lsborder=True)
        assert a.tolist() == [0, 1, None, 2, None, 3]

        # doubled
        a = BitMaskedArray.fromboolmask([True, True, False, True, False, True, True, True, False, True, False, True], [0, 1, 999, 2, 999, 3, 0, 1, 999, 2, 999, 3], maskedwhen=False, lsborder=True)
        assert a.tolist() == [0, 1, None, 2, None, 3, 0, 1, None, 2, None, 3]

    def test_indexedmasked_get(self):
        a = IndexedMaskedArray([-1, 0, -1, 1, -1, 2, -1, 4, -1, 3], [0.0, 1.1, 2.2, 3.3, 4.4])
        assert a.tolist() == [None, 0.0, None, 1.1, None, 2.2, None, 4.4, None, 3.3]
        assert [a[i] for i in range(len(a))] == [None, 0.0, None, 1.1, None, 2.2, None, 4.4, None, 3.3]
