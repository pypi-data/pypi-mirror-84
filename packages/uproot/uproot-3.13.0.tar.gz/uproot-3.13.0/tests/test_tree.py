#!/usr/bin/env python

# BSD 3-Clause License; see https://github.com/scikit-hep/uproot/blob/master/LICENSE

import os
from collections import namedtuple

import numpy
import pytest

import awkward
import uproot

def basest(array):
    while getattr(array, "base", None) is not None:
        array = array.base
    return array

class Test(object):
    ###################################################### double32

    def test_double32(self):
        t = uproot.open("tests/samples/demo-double32.root")["T"]
        fD64 = t.array("fD64")
        fF32 = t.array("fF32")
        fI32 = t.array("fI32")
        fI30 = t.array("fI30")
        fI28 = t.array("fI28")
        ratio_fF32 = fF32 / fD64
        ratio_fI32 = fI32 / fD64
        ratio_fI30 = fI30 / fD64
        ratio_fI28 = fI28 / fD64
        assert ratio_fF32.min() > 0.9999 and ratio_fF32.max() < 1.0001
        assert ratio_fI32.min() > 0.9999 and ratio_fI32.max() < 1.0001
        assert ratio_fI30.min() > 0.9999 and ratio_fI30.max() < 1.0001
        assert ratio_fI28.min() > 0.9999 and ratio_fI28.max() < 1.0001

    ###################################################### basket

    def test_flat_basket(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["i8"]
        interpretation = branch._normalize_interpretation(None, awkward)
        entrystart, entrystop = uproot.tree._normalize_entrystartstop(branch.numentries, None, None)
        local_entrystart, local_entrystop = branch._localentries(0, entrystart, entrystop)

        one = branch._basket(0, interpretation, local_entrystart, local_entrystop, awkward, None, None)
        two = branch._basket(0, interpretation, local_entrystart, local_entrystop, awkward, None, None)
        assert numpy.array_equal(one, numpy.array([-15, -14, -13], dtype=">i8"))
        assert basest(one) is basest(two)

        three = branch.basket(0)
        assert numpy.array_equal(three, numpy.array([-15, -14, -13], dtype=">i8"))
        assert basest(one) is not basest(three)

        buf = numpy.zeros(10, dtype=numpy.float64)
        four = branch.basket(0, interpretation.toarray(buf))
        assert numpy.array_equal(four, numpy.array([-15, -14, -13], dtype=">i8"))
        assert basest(four) is buf

    def test_regular_basket(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["ai8"]
        interpretation = branch._normalize_interpretation(None, awkward)
        entrystart, entrystop = uproot.tree._normalize_entrystartstop(branch.numentries, None, None)
        local_entrystart, local_entrystop = branch._localentries(0, entrystart, entrystop)

        one = branch._basket(0, interpretation, local_entrystart, local_entrystop, awkward, None, None)
        two = branch._basket(0, interpretation, local_entrystart, local_entrystop, awkward, None, None)
        assert numpy.array_equal(one, numpy.array([[-14, -13, -12]], dtype=">i8"))
        assert basest(one) is basest(two)

        three = branch.basket(0)
        assert numpy.array_equal(three, numpy.array([[-14, -13, -12]], dtype=">i8"))
        assert basest(one) is not basest(three)

        assert branch.basket(0, interpretation.to(todims=(3,))).shape == (1, 3)
        assert branch.basket(0, interpretation.to(todims=())).shape == (3,)
        assert branch.basket(0, interpretation.to(todims=(1,))).shape == (3, 1)
        assert branch.basket(0, interpretation.to(todims=(1, 1))).shape == (3, 1, 1)
        assert branch.basket(0, interpretation.to(todims=(1, 3))).shape == (1, 1, 3)

        buf = numpy.zeros(10, dtype=numpy.float64)
        four = branch.basket(0, interpretation.toarray(buf))
        assert numpy.array_equal(four, numpy.array([-14, -13, -12], dtype=">i8"))
        assert basest(four) is buf

    def test_irregular_basket(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["Ai8"]
        interpretation = branch._normalize_interpretation(None, awkward)
        entrystart, entrystop = uproot.tree._normalize_entrystartstop(branch.numentries, None, None)
        local_entrystart, local_entrystop = branch._localentries(0, entrystart, entrystop)

        one = branch._basket(0, interpretation, local_entrystart, local_entrystop, awkward, None, None)
        two = branch._basket(0, interpretation, local_entrystart, local_entrystop, awkward, None, None)
        assert numpy.array_equal(one[0], numpy.array([], dtype=">i8"))
        assert numpy.array_equal(one[1], numpy.array([-15], dtype=">i8"))
        assert basest(one.content) is basest(two.content)

        three = branch.basket(0)
        assert numpy.array_equal(three[0], numpy.array([], dtype=">i8"))
        assert numpy.array_equal(three[1], numpy.array([-15], dtype=">i8"))

    def test_strings_basket(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["str"]
        interpretation = branch._normalize_interpretation(None, awkward)
        entrystart, entrystop = uproot.tree._normalize_entrystartstop(branch.numentries, None, None)
        local_entrystart, local_entrystop = branch._localentries(0, entrystart, entrystop)

        one = branch.basket(0, interpretation, local_entrystart, local_entrystop)
        two = branch.basket(0, interpretation, local_entrystart, local_entrystop)

        assert one.tolist() == [b"hey-0", b"hey-1", b"hey-2", b"hey-3", b"hey-4", b"hey-5"]
        assert basest(one.content.content) is not basest(two.content.content)

        three = branch.basket(0)
        assert three.tolist() == [b"hey-0", b"hey-1", b"hey-2", b"hey-3", b"hey-4", b"hey-5"]

    ###################################################### baskets

    def test_flat_baskets(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["i8"]
        expectation = [[-15, -14, -13], [-12, -11, -10], [-9, -8, -7], [-6, -5, -4], [-3, -2, -1], [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14]]
        assert [x.tolist() for x in branch.baskets()] == expectation
        assert [x.tolist() for x in branch.iterate_baskets()] == expectation

    def test_regular_baskets(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["ai8"]
        expectation = [[[-14, -13, -12]], [[-13, -12, -11]], [[-12, -11, -10]], [[-11, -10, -9]], [[-10, -9, -8]], [[-9, -8, -7]], [[-8, -7, -6]], [[-7, -6, -5]], [[-6, -5, -4]], [[-5, -4, -3]], [[-4, -3, -2]], [[-3, -2, -1]], [[-2, -1, 0]], [[-1, 0, 1]], [[0, 1, 2]], [[1, 2, 3]], [[2, 3, 4]], [[3, 4, 5]], [[4, 5, 6]], [[5, 6, 7]], [[6, 7, 8]], [[7, 8, 9]], [[8, 9, 10]], [[9, 10, 11]], [[10, 11, 12]], [[11, 12, 13]], [[12, 13, 14]], [[13, 14, 15]], [[14, 15, 16]], [[15, 16, 17]]]
        assert [x.tolist() for x in branch.baskets()] == expectation
        assert [x.tolist() for x in branch.iterate_baskets()] == expectation

    def test_irregular_baskets(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["Ai8"]
        expectation = [[[], [-15]], [[-15, -13]], [[-15, -13, -11]], [[-15, -13, -11, -9]], [[], [-10]], [[-10, -8]], [[-10, -8, -6]], [[-10, -8, -6, -4]], [[], [-5]], [[-5, -3]], [[-5, -3, -1]], [[-5, -3, -1, 1]], [[], [0]], [[0, 2]], [[0, 2, 4]], [[0, 2, 4, 6]], [[], [5]], [[5, 7]], [[5, 7, 9]], [[5, 7, 9, 11]], [[], [10]], [[10, 12]], [[10, 12, 14]], [[10, 12, 14, 16]]]
        assert [len(y) for x in expectation for y in x] == [0, 1, 2, 3, 4] * 6
        assert [x.tolist() for x in branch.baskets()] == expectation
        assert [x.tolist() for x in branch.iterate_baskets()] == expectation

    def test_strings_baskets(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["str"]
        expectation = [[b"hey-0", b"hey-1", b"hey-2", b"hey-3", b"hey-4", b"hey-5"], [b"hey-6", b"hey-7", b"hey-8", b"hey-9", b"hey-10"], [b"hey-11", b"hey-12", b"hey-13", b"hey-14", b"hey-15"], [b"hey-16", b"hey-17", b"hey-18", b"hey-19", b"hey-20"], [b"hey-21", b"hey-22", b"hey-23", b"hey-24", b"hey-25"], [b"hey-26", b"hey-27", b"hey-28", b"hey-29"]]
        assert [x.tolist() for x in branch.baskets()] == expectation
        assert [x.tolist() for x in branch.iterate_baskets()] == expectation

    ###################################################### array

    def test_flat_array(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["i8"]
        expectation = [-15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        for entrystart, entrystop in [(None, None), (1, None), (1, 2), (1, 10), (10, 11), (10, 20), (6, 12), (6, 13)]:
            assert branch.array(entrystart=entrystart, entrystop=entrystop).tolist() == expectation[entrystart:entrystop]

    def test_regular_array(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["ai8"]
        expectation = [[-14, -13, -12], [-13, -12, -11], [-12, -11, -10], [-11, -10, -9], [-10, -9, -8], [-9, -8, -7], [-8, -7, -6], [-7, -6, -5], [-6, -5, -4], [-5, -4, -3], [-4, -3, -2], [-3, -2, -1], [-2, -1, 0], [-1, 0, 1], [0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8], [7, 8, 9], [8, 9, 10], [9, 10, 11], [10, 11, 12], [11, 12, 13], [12, 13, 14], [13, 14, 15], [14, 15, 16], [15, 16, 17]]
        for entrystart, entrystop in [(None, None), (1, None), (1, 2), (1, 10), (10, 11), (10, 20), (6, 12), (6, 13)]:
            assert branch.array(entrystart=entrystart, entrystop=entrystop).tolist() == expectation[entrystart:entrystop]

    def test_irregular_array(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["Ai8"]
        expectation = [[], [-15], [-15, -13], [-15, -13, -11], [-15, -13, -11, -9], [], [-10], [-10, -8], [-10, -8, -6], [-10, -8, -6, -4], [], [-5], [-5, -3], [-5, -3, -1], [-5, -3, -1, 1], [], [0], [0, 2], [0, 2, 4], [0, 2, 4, 6], [], [5], [5, 7], [5, 7, 9], [5, 7, 9, 11], [], [10], [10, 12], [10, 12, 14], [10, 12, 14, 16]]
        assert [len(x) for x in expectation] == [0, 1, 2, 3, 4] * 6
        for entrystart, entrystop in [(None, None), (1, None), (1, 2), (1, 10), (10, 11), (10, 20), (6, 12), (6, 13)]:
            assert branch.array(entrystart=entrystart, entrystop=entrystop).tolist() == expectation[entrystart:entrystop]

    def test_strings_array(self):
        branch = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]["str"]
        expectation = [b"hey-0", b"hey-1", b"hey-2", b"hey-3", b"hey-4", b"hey-5", b"hey-6", b"hey-7", b"hey-8", b"hey-9", b"hey-10", b"hey-11", b"hey-12", b"hey-13", b"hey-14", b"hey-15", b"hey-16", b"hey-17", b"hey-18", b"hey-19", b"hey-20", b"hey-21", b"hey-22", b"hey-23", b"hey-24", b"hey-25", b"hey-26", b"hey-27", b"hey-28", b"hey-29"]
        for entrystart, entrystop in [(None, None), (1, None), (1, 2), (1, 10), (10, 11), (10, 20), (6, 12), (6, 13)]:
            assert branch.array(entrystart=entrystart, entrystop=entrystop).tolist() == expectation[entrystart:entrystop]

    ###################################################### iterate

    def test_flat_iterate(self):
        tree = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]
        expectation = [-15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        for n in 1000, 5, 6, 7:
            assert [x.tolist() for (x,) in tree.iterate("i8", n, outputtype=tuple)] == [expectation[x : x + n] for x in range(0, len(expectation), n)]

    def test_regular_iterate(self):
        tree = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]
        expectation = [[-14, -13, -12], [-13, -12, -11], [-12, -11, -10], [-11, -10, -9], [-10, -9, -8], [-9, -8, -7], [-8, -7, -6], [-7, -6, -5], [-6, -5, -4], [-5, -4, -3], [-4, -3, -2], [-3, -2, -1], [-2, -1, 0], [-1, 0, 1], [0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8], [7, 8, 9], [8, 9, 10], [9, 10, 11], [10, 11, 12], [11, 12, 13], [12, 13, 14], [13, 14, 15], [14, 15, 16], [15, 16, 17]]
        for n in 1000, 5, 6, 7:
            assert [x.tolist() for (x,) in tree.iterate("ai8", n, outputtype=tuple)] == [expectation[x : x + n] for x in range(0, len(expectation), n)]

    def test_irregular_iterate(self):
        tree = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]
        expectation = [[], [-15], [-15, -13], [-15, -13, -11], [-15, -13, -11, -9], [], [-10], [-10, -8], [-10, -8, -6], [-10, -8, -6, -4], [], [-5], [-5, -3], [-5, -3, -1], [-5, -3, -1, 1], [], [0], [0, 2], [0, 2, 4], [0, 2, 4, 6], [], [5], [5, 7], [5, 7, 9], [5, 7, 9, 11], [], [10], [10, 12], [10, 12, 14], [10, 12, 14, 16]]
        for n in 1000, 5, 6, 7:
            assert [x.tolist() for (x,) in tree.iterate("Ai8", n, outputtype=tuple)] == [expectation[x : x + n] for x in range(0, len(expectation), n)]

    def test_strings_iterate(self):
        tree = uproot.open("tests/samples/sample-6.10.05-uncompressed.root")["sample"]
        expectation = [b"hey-0", b"hey-1", b"hey-2", b"hey-3", b"hey-4", b"hey-5", b"hey-6", b"hey-7", b"hey-8", b"hey-9", b"hey-10", b"hey-11", b"hey-12", b"hey-13", b"hey-14", b"hey-15", b"hey-16", b"hey-17", b"hey-18", b"hey-19", b"hey-20", b"hey-21", b"hey-22", b"hey-23", b"hey-24", b"hey-25", b"hey-26", b"hey-27", b"hey-28", b"hey-29"]
        for n in 1000, 5, 6, 7:
            assert [x.tolist() for (x,) in tree.iterate("str", n, outputtype=tuple)] == [expectation[x : x + n] for x in range(0, len(expectation), n)]

    ###################################################### old tests

    def test_branch_array(self):
        file = uproot.open("tests/samples/simple.root")
        repr(file)

        tree = file["tree"]
        repr(tree)
        repr(tree["one"])

        assert tree["one"].array().tolist() == [1, 2, 3, 4]
        assert tree["two"].array().tolist() == numpy.array([1.1, 2.2, 3.3, 4.4], dtype=numpy.float32).tolist()
        assert tree["three"].array().tolist() == [b"uno", b"dos", b"tres", b"quatro"]

        assert tree["one"].array().tolist() == [1, 2, 3, 4]
        assert tree["two"].array().tolist() == numpy.array([1.1, 2.2, 3.3, 4.4], dtype=numpy.float32).tolist()
        assert tree["three"].array().tolist() == [b"uno", b"dos", b"tres", b"quatro"]

        tree = file["tree"]
        assert tree["one"].array().tolist() == [1, 2, 3, 4]
        assert tree["two"].array().tolist() == numpy.array([1.1, 2.2, 3.3, 4.4], dtype=numpy.float32).tolist()
        assert tree["three"].array().tolist() == [b"uno", b"dos", b"tres", b"quatro"]

    def test_tree_arrays(self):
        file = uproot.open("tests/samples/simple.root")

        tree = file["tree"]
        arrays = tree.arrays()
        assert arrays[b"one"].tolist() == [1, 2, 3, 4]
        assert arrays[b"two"].tolist() == numpy.array([1.1, 2.2, 3.3, 4.4], dtype=numpy.float32).tolist()
        assert arrays[b"three"].tolist() == [b"uno", b"dos", b"tres", b"quatro"]

        # get arrays again
        arrays = tree.arrays()
        assert arrays[b"one"].tolist() == [1, 2, 3, 4]
        assert arrays[b"two"].tolist() == numpy.array([1.1, 2.2, 3.3, 4.4], dtype=numpy.float32).tolist()
        assert arrays[b"three"].tolist() == [b"uno", b"dos", b"tres", b"quatro"]

        # get tree again
        tree = file["tree"]
        arrays = tree.arrays()
        assert arrays[b"one"].tolist() == [1, 2, 3, 4]
        assert arrays[b"two"].tolist() == numpy.array([1.1, 2.2, 3.3, 4.4], dtype=numpy.float32).tolist()
        assert arrays[b"three"].tolist() == [b"uno", b"dos", b"tres", b"quatro"]

    def test_tree_arrays_namedecode(self):
        file = uproot.open("tests/samples/simple.root")

        tree = file["tree"]
        arrays = tree.arrays(namedecode="utf-8")
        assert arrays["one"].tolist() == [1, 2, 3, 4]
        assert arrays["two"].tolist() == numpy.array([1.1, 2.2, 3.3, 4.4], dtype=numpy.float32).tolist()
        assert arrays["three"].tolist() == [b"uno", b"dos", b"tres", b"quatro"]

    def test_tree_iterator1(self):
        # one big array
        for arrays in uproot.open("tests/samples/foriter.root")["foriter"].iterate(entrysteps=1000):
            assert arrays[b"data"].tolist() == list(range(46))

        # size is equal to basket size (for most baskets)
        i = 0
        for arrays in uproot.open("tests/samples/foriter.root")["foriter"].iterate(entrysteps=6):
            assert arrays[b"data"].tolist() == list(range(i, min(i + 6, 46)))
            i += 6

        # size is smaller
        i = 0
        for arrays in uproot.open("tests/samples/foriter.root")["foriter"].iterate(entrysteps=3):
            assert arrays[b"data"].tolist() == list(range(i, min(i + 3, 46)))
            i += 3
        i = 0
        for arrays in uproot.open("tests/samples/foriter.root")["foriter"].iterate(entrysteps=4):
            assert arrays[b"data"].tolist() == list(range(i, min(i + 4, 46)))
            i += 4

        # size is larger
        i = 0
        for arrays in uproot.open("tests/samples/foriter.root")["foriter"].iterate(entrysteps=12):
            assert arrays[b"data"].tolist() == list(range(i, min(i + 12, 46)))
            i += 12
        i = 0
        for arrays in uproot.open("tests/samples/foriter.root")["foriter"].iterate(entrysteps=10):
            assert arrays[b"data"].tolist() == list(range(i, min(i + 10, 46)))
            i += 10

        # singleton case
        i = 0
        for arrays in uproot.open("tests/samples/foriter.root")["foriter"].iterate(entrysteps=1):
            assert arrays[b"data"].tolist() == list(range(i, min(i + 1, 46)))
            i += 1

    def test_tree_iterator2(self):
        words = [b"zero", b"one", b"two", b"three", b"four", b"five", b"six", b"seven", b"eight", b"nine", b"ten", b"eleven", b"twelve", b"thirteen", b"fourteen", b"fifteen", b"sixteen", b"seventeen", b"eighteen", b"ninteen", b"twenty", b"twenty-one", b"twenty-two", b"twenty-three", b"twenty-four", b"twenty-five", b"twenty-six", b"twenty-seven", b"twenty-eight", b"twenty-nine", b"thirty"]

        # one big array
        for arrays in uproot.open("tests/samples/foriter2.root")["foriter2"].iterate(entrysteps=1000):
            assert arrays[b"data"].tolist() == words

        # size is equal to basket size (for most baskets)
        i = 0
        for arrays in uproot.open("tests/samples/foriter2.root")["foriter2"].iterate(entrysteps=6):
            assert arrays[b"data"].tolist() == words[i:i + 6]
            i += 6

        # size is smaller
        i = 0
        for arrays in uproot.open("tests/samples/foriter2.root")["foriter2"].iterate(entrysteps=3):
            assert arrays[b"data"].tolist() == words[i:i + 3]
            i += 3
        i = 0
        for arrays in uproot.open("tests/samples/foriter2.root")["foriter2"].iterate(entrysteps=4):
            assert arrays[b"data"].tolist() == words[i:i + 4]
            i += 4

        # size is larger
        i = 0
        for arrays in uproot.open("tests/samples/foriter2.root")["foriter2"].iterate(entrysteps=12):
            assert arrays[b"data"].tolist() == words[i:i + 12]
            i += 12
        i = 0
        for arrays in uproot.open("tests/samples/foriter2.root")["foriter2"].iterate(entrysteps=10):
            assert arrays[b"data"].tolist() == words[i:i + 10]
            i += 10

        # singleton case
        i = 0
        for arrays in uproot.open("tests/samples/foriter2.root")["foriter2"].iterate(entrysteps=1):
            assert arrays[b"data"].tolist() == words[i:i + 1]
            i += 1

    def test_tree_iterator3(self):
        source = list(range(46))

        # one big array
        for arrays in uproot.iterate(["tests/samples/foriter.root", "tests/samples/foriter.root"], "foriter", entrysteps=1000):
            assert arrays[b"data"].tolist() == source

        # size is equal to basket size (for most baskets)
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter.root", "tests/samples/foriter.root"], "foriter", entrysteps=6):
            assert arrays[b"data"].tolist() == source[i : i + 6]
            i += 6
            if i > 45: i = 0

        # size is smaller
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter.root", "tests/samples/foriter.root"], "foriter", entrysteps=3):
            assert arrays[b"data"].tolist() == source[i : i + 3]
            i += 3
            if i > 45: i = 0
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter.root", "tests/samples/foriter.root"], "foriter", entrysteps=4):
            assert arrays[b"data"].tolist() == source[i : i + 4]
            i += 4
            if i > 45: i = 0

        # size is larger
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter.root", "tests/samples/foriter.root"], "foriter", entrysteps=12):
            assert arrays[b"data"].tolist() == source[i : i + 12]
            i += 12
            if i > 45: i = 0
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter.root", "tests/samples/foriter.root"], "foriter", entrysteps=10):
            assert arrays[b"data"].tolist() == source[i : i + 10]
            i += 10
            if i > 45: i = 0

        # singleton case
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter.root", "tests/samples/foriter.root"], "foriter", entrysteps=1):
            assert arrays[b"data"].tolist() == source[i : i + 1]
            i += 1
            if i > 45: i = 0

    def test_tree_iterator4(self):
        words2 = [b"zero", b"one", b"two", b"three", b"four", b"five", b"six", b"seven", b"eight", b"nine", b"ten", b"eleven", b"twelve", b"thirteen", b"fourteen", b"fifteen", b"sixteen", b"seventeen", b"eighteen", b"ninteen", b"twenty", b"twenty-one", b"twenty-two", b"twenty-three", b"twenty-four", b"twenty-five", b"twenty-six", b"twenty-seven", b"twenty-eight", b"twenty-nine", b"thirty"]

        # one big array
        for arrays in uproot.iterate(["tests/samples/foriter2.root", "tests/samples/foriter2.root"], "foriter2", entrysteps=1000):
            assert arrays[b"data"].tolist() == words2

        # size is equal to basket size (for most baskets)
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter2.root", "tests/samples/foriter2.root"], "foriter2", entrysteps=6):
            assert arrays[b"data"].tolist() == words2[i : i + 6]
            i += 6
            if i > 30: i = 0

        # size is smaller
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter2.root", "tests/samples/foriter2.root"], "foriter2", entrysteps=3):
            assert arrays[b"data"].tolist() == words2[i : i + 3]
            i += 3
            if i > 30: i = 0
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter2.root", "tests/samples/foriter2.root"], "foriter2", entrysteps=4):
            assert arrays[b"data"].tolist() == words2[i : i + 4]
            i += 4
            if i > 30: i = 0

        # size is larger
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter2.root", "tests/samples/foriter2.root"], "foriter2", entrysteps=12):
            assert arrays[b"data"].tolist() == words2[i : i + 12]
            i += 12
            if i > 30: i = 0
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter2.root", "tests/samples/foriter2.root"], "foriter2", entrysteps=10):
            assert arrays[b"data"].tolist() == words2[i : i + 10]
            i += 10
            if i > 30: i = 0

        # singleton case
        i = 0
        for arrays in uproot.iterate(["tests/samples/foriter2.root", "tests/samples/foriter2.root"], "foriter2", entrysteps=1):
            assert arrays[b"data"].tolist() == words2[i : i + 1]
            i += 1
            if i > 30: i = 0

    def test_directories(self):
        file = uproot.open("tests/samples/nesteddirs.root")

        assert [(n, cls._classname) for n, cls in file.classes()] == [(b"one;1", b"TDirectory"), (b"three;1", b"TDirectory")]
        assert [(n, cls._classname) for n, cls in file.allclasses()] == [(b"one;1", b"TDirectory"), (b"one/two;1", b"TDirectory"), (b"one/two/tree;1", b"TTree"), (b"one/tree;1", b"TTree"), (b"three;1", b"TDirectory"), (b"three/tree;1", b"TTree")]

        assert list(file["one"]["tree"].keys()) == [b"one", b"two", b"three"]
        assert list(file["one"].get("tree", 1).keys()) == [b"one", b"two", b"three"]
        assert list(file["one/tree;1"].keys()) == [b"one", b"two", b"three"]
        assert list(file["one/two/tree;1"].keys()) == [b"Int32", b"Int64", b"UInt32", b"UInt64", b"Float32", b"Float64", b"Str", b"ArrayInt32", b"ArrayInt64", b"ArrayUInt32", b"ArrayUInt64", b"ArrayFloat32", b"ArrayFloat64", b"N", b"SliceInt32", b"SliceInt64", b"SliceUInt32", b"SliceUInt64", b"SliceFloat32", b"SliceFloat64"]
        assert list(file["three/tree;1"].keys()) == [b"evt"]

        assert dict((name, array.tolist()) for name, array in file["one/tree"].arrays(["one", "two", "three"]).items()) == {b"one": [1, 2, 3, 4], b"two": [1.100000023841858, 2.200000047683716, 3.299999952316284, 4.400000095367432], b"three": [b"uno", b"dos", b"tres", b"quatro"]}
        assert file["one/two/tree"].array("Int32").shape == (100,)
        assert file["three/tree"].array("I32").shape == (100,)

        file = uproot.open("tests/samples/nesteddirs.root")

        assert list(file["one/tree"].keys()) == [b"one", b"two", b"three"]
        assert list(file["one/two/tree"].keys()) == [b"Int32", b"Int64", b"UInt32", b"UInt64", b"Float32", b"Float64", b"Str", b"ArrayInt32", b"ArrayInt64", b"ArrayUInt32", b"ArrayUInt64", b"ArrayFloat32", b"ArrayFloat64", b"N", b"SliceInt32", b"SliceInt64", b"SliceUInt32", b"SliceUInt64", b"SliceFloat32", b"SliceFloat64"]
        assert list(file["three/tree"].keys()) == [b"evt"]

        assert dict((name, array.tolist()) for name, array in file["one/tree;1"].arrays(["one", "two", "three"]).items()) == {b"one": [1, 2, 3, 4], b"two": [1.100000023841858, 2.200000047683716, 3.299999952316284, 4.400000095367432], b"three": [b"uno", b"dos", b"tres", b"quatro"]}
        assert file["one/two/tree;1"].array("Int32").shape == (100,)
        assert file["three/tree;1"].array("I32").shape == (100,)

    def test_cast(self):
        tree = uproot.open("tests/samples/Zmumu.root")["events"]
        one = numpy.cast[numpy.int32](numpy.floor(tree.array("M")))
        two = tree.array("M", numpy.int32)
        assert one.dtype == two.dtype
        assert one.shape == two.shape
        assert numpy.array_equal(one, two)

        for (one,) in tree.iterate("M", 10000, outputtype=tuple):
            one = numpy.cast[numpy.int32](numpy.floor(one))
        for (two,) in tree.iterate({"M": numpy.int32}, 10000, outputtype=tuple):
            pass
        assert one.dtype == two.dtype
        assert one.shape == two.shape
        assert numpy.array_equal(one, two)

    def test_pass_array(self):
        tree = uproot.open("tests/samples/Zmumu.root")["events"]
        one = numpy.cast[numpy.int32](numpy.floor(tree.array("M")))
        two = numpy.zeros(one.shape, dtype=one.dtype)
        tree.array("M", two)
        assert numpy.array_equal(one, two)

        for (one,) in tree.iterate("M", 10000, outputtype=tuple):
            one = numpy.cast[numpy.int32](numpy.floor(one))
            two = numpy.zeros(one.shape, dtype=one.dtype)
            for (two,) in tree.iterate({"M": numpy.int32}, 10000, outputtype=tuple):
                assert numpy.array_equal(one, two)

    def test_outputtype(self):
        tree = uproot.open("tests/samples/simple.root")["tree"]

        arrays = tree.arrays(["three", "two", "one"], outputtype=dict)
        assert isinstance(arrays, dict)
        assert arrays[b"one"].tolist() == [1, 2, 3, 4]
        assert arrays[b"three"].tolist() == [b"uno", b"dos", b"tres", b"quatro"]

        arrays = tree.arrays(["three", "two", "one"], outputtype=tuple)
        assert isinstance(arrays, tuple)
        assert arrays[2].tolist() == [1, 2, 3, 4]
        assert arrays[0].tolist() == [b"uno", b"dos", b"tres", b"quatro"]

        arrays = tree.arrays(["three", "two", "one"], outputtype=namedtuple)
        assert arrays.one.tolist() == [1, 2, 3, 4]
        assert arrays.three.tolist() == [b"uno", b"dos", b"tres", b"quatro"]

        arrays = tree.arrays(["three", "two", "one"], outputtype=list)
        assert isinstance(arrays, list)
        assert arrays[2].tolist() == [1, 2, 3, 4]
        assert arrays[0].tolist() == [b"uno", b"dos", b"tres", b"quatro"]

        class Awesome(object):
            def __init__(self, one, two, three):
                self.one = one
                self.two = two
                self.three = three

        arrays = tree.arrays(["one", "two", "three"], outputtype=Awesome)
        assert isinstance(arrays, Awesome)
        assert arrays.one.tolist() == [1, 2, 3, 4]
        assert arrays.three.tolist() == [b"uno", b"dos", b"tres", b"quatro"]

        class MyList(list):
            pass

        class MyTuple(tuple):
            pass

        arrays = tree.arrays(["three", "two", "one"], outputtype=MyList)
        assert isinstance(arrays, MyList)
        assert arrays[2].tolist() == [1, 2, 3, 4]
        assert arrays[0].tolist() == [b"uno", b"dos", b"tres", b"quatro"]

        arrays = tree.arrays(["three", "two", "one"], outputtype=MyTuple)
        assert isinstance(arrays, MyTuple)

    def test_tree_lazy(self):
        tree = uproot.open("tests/samples/sample-5.30.00-uncompressed.root")["sample"]

        for branchname in b"u1", b"i8", b"Ai8", b"f4", b"af4":
            strict = tree[branchname].array()

            lazy = tree[branchname].lazyarray()
            for i in range(len(lazy)):
                assert lazy[i].tolist() == strict[i].tolist()

            lazy = tree[branchname].lazyarray()
            for i in range(len(lazy), 0, -1):
                assert lazy[i - 1].tolist() == strict[i - 1].tolist()

            lazy = tree[branchname].lazyarray()
            for i in range(len(lazy)):
                assert lazy[i : i + 3].tolist() == strict[i : i + 3].tolist()

            lazy = tree[branchname].lazyarray()
            for i in range(len(lazy), 0, -1):
                assert lazy[i - 1 : i + 3].tolist() == strict[i - 1 : i + 3].tolist()

    def test_tree_lazy2(self):
        tree = uproot.open("tests/samples/sample-5.30.00-uncompressed.root")["sample"]
        lazy = tree.lazyarrays()

        for branchname in "u1", "i8", "Ai8", "f4", "af4":
            strict = tree[branchname.encode()].array()

            for i in range(len(lazy)):
                assert lazy[branchname][i].tolist() == strict[i].tolist()

            for i in range(len(lazy), 0, -1):
                assert lazy[branchname][i - 1].tolist() == strict[i - 1].tolist()

            for i in range(len(lazy)):
                assert lazy[branchname][i : i + 3].tolist() == strict[i : i + 3].tolist()

            for i in range(len(lazy), 0, -1):
                assert lazy[branchname][i - 1 : i + 3].tolist() == strict[i - 1 : i + 3].tolist()

    def test_tree_lazy3(self):
        lazy = uproot.lazyarrays(["tests/samples/sample-5.29.02-uncompressed.root", "tests/samples/sample-5.30.00-uncompressed.root"], "sample")

        assert lazy["u1"].tolist() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        assert lazy["i8"].tolist() == [-15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        assert lazy["Ai8"].tolist() == [[], [-15], [-15, -13], [-15, -13, -11], [-15, -13, -11, -9], [], [-10], [-10, -8], [-10, -8, -6], [-10, -8, -6, -4], [], [-5], [-5, -3], [-5, -3, -1], [-5, -3, -1, 1], [], [0], [0, 2], [0, 2, 4], [0, 2, 4, 6], [], [5], [5, 7], [5, 7, 9], [5, 7, 9, 11], [], [10], [10, 12], [10, 12, 14], [10, 12, 14, 16], [], [-15], [-15, -13], [-15, -13, -11], [-15, -13, -11, -9], [], [-10], [-10, -8], [-10, -8, -6], [-10, -8, -6, -4], [], [-5], [-5, -3], [-5, -3, -1], [-5, -3, -1, 1], [], [0], [0, 2], [0, 2, 4], [0, 2, 4, 6], [], [5], [5, 7], [5, 7, 9], [5, 7, 9, 11], [], [10], [10, 12], [10, 12, 14], [10, 12, 14, 16]]
        assert lazy["f4"].tolist() == [-14.899999618530273, -13.899999618530273, -12.899999618530273, -11.899999618530273, -10.899999618530273, -9.899999618530273, -8.899999618530273, -7.900000095367432, -6.900000095367432, -5.900000095367432, -4.900000095367432, -3.9000000953674316, -2.9000000953674316, -1.899999976158142, -0.8999999761581421, 0.10000000149011612, 1.100000023841858, 2.0999999046325684, 3.0999999046325684, 4.099999904632568, 5.099999904632568, 6.099999904632568, 7.099999904632568, 8.100000381469727, 9.100000381469727, 10.100000381469727, 11.100000381469727, 12.100000381469727, 13.100000381469727, 14.100000381469727, -14.899999618530273, -13.899999618530273, -12.899999618530273, -11.899999618530273, -10.899999618530273, -9.899999618530273, -8.899999618530273, -7.900000095367432, -6.900000095367432, -5.900000095367432, -4.900000095367432, -3.9000000953674316, -2.9000000953674316, -1.899999976158142, -0.8999999761581421, 0.10000000149011612, 1.100000023841858, 2.0999999046325684, 3.0999999046325684, 4.099999904632568, 5.099999904632568, 6.099999904632568, 7.099999904632568, 8.100000381469727, 9.100000381469727, 10.100000381469727, 11.100000381469727, 12.100000381469727, 13.100000381469727, 14.100000381469727]
        assert lazy["af4"].tolist() == [[-13.899999618530273, -12.899999618530273, -11.899999618530273], [-12.899999618530273, -11.899999618530273, -10.899999618530273], [-11.899999618530273, -10.899999618530273, -9.899999618530273], [-10.899999618530273, -9.899999618530273, -8.899999618530273], [-9.899999618530273, -8.899999618530273, -7.900000095367432], [-8.899999618530273, -7.900000095367432, -6.900000095367432], [-7.900000095367432, -6.900000095367432, -5.900000095367432], [-6.900000095367432, -5.900000095367432, -4.900000095367432], [-5.900000095367432, -4.900000095367432, -3.9000000953674316], [-4.900000095367432, -3.9000000953674316, -2.9000000953674316], [-3.9000000953674316, -2.9000000953674316, -1.899999976158142], [-2.9000000953674316, -1.899999976158142, -0.8999999761581421], [-1.899999976158142, -0.8999999761581421, 0.10000000149011612], [-0.8999999761581421, 0.10000000149011612, 1.100000023841858], [0.10000000149011612, 1.100000023841858, 2.0999999046325684], [1.100000023841858, 2.0999999046325684, 3.0999999046325684], [2.0999999046325684, 3.0999999046325684, 4.099999904632568], [3.0999999046325684, 4.099999904632568, 5.099999904632568], [4.099999904632568, 5.099999904632568, 6.099999904632568], [5.099999904632568, 6.099999904632568, 7.099999904632568], [6.099999904632568, 7.099999904632568, 8.100000381469727], [7.099999904632568, 8.100000381469727, 9.100000381469727], [8.100000381469727, 9.100000381469727, 10.100000381469727], [9.100000381469727, 10.100000381469727, 11.100000381469727], [10.100000381469727, 11.100000381469727, 12.100000381469727], [11.100000381469727, 12.100000381469727, 13.100000381469727], [12.100000381469727, 13.100000381469727, 14.100000381469727], [13.100000381469727, 14.100000381469727, 15.100000381469727], [14.100000381469727, 15.100000381469727, 16.100000381469727], [15.100000381469727, 16.100000381469727, 17.100000381469727], [-13.899999618530273, -12.899999618530273, -11.899999618530273], [-12.899999618530273, -11.899999618530273, -10.899999618530273], [-11.899999618530273, -10.899999618530273, -9.899999618530273], [-10.899999618530273, -9.899999618530273, -8.899999618530273], [-9.899999618530273, -8.899999618530273, -7.900000095367432], [-8.899999618530273, -7.900000095367432, -6.900000095367432], [-7.900000095367432, -6.900000095367432, -5.900000095367432], [-6.900000095367432, -5.900000095367432, -4.900000095367432], [-5.900000095367432, -4.900000095367432, -3.9000000953674316], [-4.900000095367432, -3.9000000953674316, -2.9000000953674316], [-3.9000000953674316, -2.9000000953674316, -1.899999976158142], [-2.9000000953674316, -1.899999976158142, -0.8999999761581421], [-1.899999976158142, -0.8999999761581421, 0.10000000149011612], [-0.8999999761581421, 0.10000000149011612, 1.100000023841858], [0.10000000149011612, 1.100000023841858, 2.0999999046325684], [1.100000023841858, 2.0999999046325684, 3.0999999046325684], [2.0999999046325684, 3.0999999046325684, 4.099999904632568], [3.0999999046325684, 4.099999904632568, 5.099999904632568], [4.099999904632568, 5.099999904632568, 6.099999904632568], [5.099999904632568, 6.099999904632568, 7.099999904632568], [6.099999904632568, 7.099999904632568, 8.100000381469727], [7.099999904632568, 8.100000381469727, 9.100000381469727], [8.100000381469727, 9.100000381469727, 10.100000381469727], [9.100000381469727, 10.100000381469727, 11.100000381469727], [10.100000381469727, 11.100000381469727, 12.100000381469727], [11.100000381469727, 12.100000381469727, 13.100000381469727], [12.100000381469727, 13.100000381469727, 14.100000381469727], [13.100000381469727, 14.100000381469727, 15.100000381469727], [14.100000381469727, 15.100000381469727, 16.100000381469727], [15.100000381469727, 16.100000381469727, 17.100000381469727]]

    def test_tree_lazy_cached(self):
        tree = uproot.open("tests/samples/sample-5.30.00-uncompressed.root")["sample"]

        cache = {}
        keycache = {}
        basketcache = {}

        for branchname in b"u1", b"i8", b"Ai8", b"f4", b"af4":
            strict = tree[branchname].array()

            lazy = tree[branchname].lazyarray(cache=cache, keycache=keycache, basketcache=basketcache)
            for i in range(len(lazy)):
                assert lazy[i].tolist() == strict[i].tolist()

            lazy = tree[branchname].lazyarray(cache=cache, keycache=keycache, basketcache=basketcache)
            for i in range(len(lazy), 0, -1):
                assert lazy[i - 1].tolist() == strict[i - 1].tolist()

            lazy = tree[branchname].lazyarray(cache=cache, keycache=keycache, basketcache=basketcache)
            for i in range(len(lazy)):
                assert lazy[i : i + 3].tolist() == strict[i : i + 3].tolist()

            lazy = tree[branchname].lazyarray(cache=cache, keycache=keycache, basketcache=basketcache)
            for i in range(len(lazy), 0, -1):
                assert lazy[i - 1 : i + 3].tolist() == strict[i - 1 : i + 3].tolist()

    @pytest.mark.parametrize("use_http", [False, True])
    def test_hist_in_tree(self, use_http):
        if use_http:
            pytest.importorskip("requests")
            tree = uproot.open("http://scikit-hep.org/uproot/examples/Event.root")["T"]
        else:
            path = os.path.join("tests", "samples", "Event.root")
            if not os.path.exists(path):
                raise pytest.skip()
            tree = uproot.open(path)["T"]
        check = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
                 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
                 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 1.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]

        assert tree.array("fH")[20].values.tolist() == check

    @pytest.mark.parametrize("use_http", [False, True])
    def test_branch_auto_interpretation(self, use_http):
        # The aim is to reduce this list in a controlled manner
        known_branches_without_interp = [
            b'event',
            b'TObject',
            b'fClosestDistance',
            b'fEvtHdr',
            b'fTracks',
            b'fTracks.fPointValue',
            b'fTriggerBits',
            b'fTriggerBits.TObject'
        ]
        if use_http:
            pytest.importorskip("requests")
            tree = uproot.open("http://scikit-hep.org/uproot/examples/Event.root")["T"]
        else:
            path = os.path.join("tests", "samples", "Event.root")
            if not os.path.exists(path):
                raise pytest.skip()
            tree = uproot.open(path)["T"]
        branches_without_interp = [b.name for b in tree.allvalues() if b.interpretation is None]
        assert branches_without_interp == known_branches_without_interp
        assert tree.array("fTracks.fTArray[3]", entrystop=10)[5][10].tolist()  == [11.03951644897461, 19.40645980834961, 34.54059982299805]
        assert tree.array("fTracks.fCharge", entrystop=10)[0][0:10].tolist()   == [1.0, 1.0, 1.0, 1.0,-1.0, 0.0, 1.0, 0.0, 0.0, 0.0]
        assert tree.array("fMatrix[4][4]", entrystop=10)[0][1].tolist()        == [-0.13630907237529755, 0.8007842898368835, 1.706235647201538, 0.0]
        assert tree.array("fTracks.fMass2", entrystop=10)[3][330:333].tolist() == [8.90625, 8.90625, 8.90625]
        assert tree.array("fTracks.fBx", entrystop=10)[9][10:13].tolist()      == [0.12298583984375, -0.2489013671875, -0.189697265625]
        assert tree.array("fTracks.fBy", entrystop=10)[9][10:13].tolist()      == [0.1998291015625, -0.0301513671875, 0.0736083984375]
        assert tree.array("fTracks.fXfirst", entrystop=10)[1][11:16].tolist()  == [-8.650390625, -2.8203125, -1.949951171875, 0.4859619140625, 3.0146484375]
        assert tree.array("fTracks.fXlast", entrystop=10)[1][11:16].tolist()   == [-2.18994140625, -2.64697265625, -8.4375, 1.594970703125, 6.40234375]
        assert tree.array("fTracks.fYfirst", entrystop=10)[2][22:26].tolist()  == [4.9921875, 8.46875, 1.679443359375, -6.927734375]
        assert tree.array("fTracks.fYlast", entrystop=10)[2][22:26].tolist()   == [-5.76171875, 13.7109375, 2.98583984375, -9.466796875]
        assert tree.array("fTracks.fZfirst", entrystop=10)[3][33:36].tolist()  == [53.84375, 52.3125, 48.296875]
        assert tree.array("fTracks.fZlast", entrystop=10)[3][33:36].tolist()   == [193.96875, 208.25, 228.40625]
        assert tree.array("fTracks.fVertex[3]", entrystop=10)[1][2].tolist()   == [0.245361328125, 0.029296875,-16.171875]

    def test_leaflist(self):
        tree = uproot.open("tests/samples/leaflist.root")["tree"]
        a = tree.array("leaflist")
        assert a["x"].tolist() == [1.1, 2.2, 3.3, 4.0, 5.5]   # yeah, I goofed up when making it
        assert a["y"].tolist() == [1, 2, 3, 4, 5]
        assert a["z"].tolist() == [ord("a"), ord("b"), ord("c"), ord("d"), ord("e")]

        pytest.importorskip("pandas")
        assert tree.pandas.df()["leaflist.x"].tolist() == [1.1, 2.2, 3.3, 4.0, 5.5]

        tree = uproot.open("tests/samples/HZZ-objects.root")["events"]
        tree.pandas.df("muonp4")
        tree.pandas.df("muonp4", flatten=False)
        df = tree.pandas.df("eventweight", entrystart=100, entrystop=200)
        index = df.index.tolist()
        assert min(index) == 100
        assert max(index) == 199
        df = tree.pandas.df("muonp4", entrystart=100, entrystop=200)
        index = df.index.get_level_values("entry").tolist()
        assert min(index) == 100
        assert max(index) == 199

    def test_mempartitions(self):
        t = uproot.open("tests/samples/sample-5.23.02-zlib.root")["sample"]
        assert list(t.mempartitions(500)) == [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20), (20, 22), (22, 24), (24, 26), (26, 28), (28, 30)]
        assert [sum(y.nbytes for y in x.values()) for x in t.iterate(entrysteps="0.5 kB")] == [693, 865, 822, 779, 951, 695, 867, 824, 781, 953, 695, 867, 824, 781, 953]
