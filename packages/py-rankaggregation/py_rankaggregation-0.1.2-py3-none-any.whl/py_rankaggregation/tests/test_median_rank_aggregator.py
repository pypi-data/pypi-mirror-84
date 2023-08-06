import os
from nose.tools import *
import pandas as pd
import unittest

import py_rankaggregation as ra

p = ra.get_install_path()

# list of lists number 1
lofls1 = [
    ['a', 'b', 'c'],
    ['a', 'b', 'c'],
    ['d', 'a', 'b', 'c'],
]

expected_medianagg1  = [('a', 1.5), ('b', 2.5), ('c', 3.5), ('d', 5.0)]

# list of lists number 2
lofls2 = [
    [('a',1.2), ('b',.2), ('c',.01)],
    [('a',10), ('b',10), ('c',1)],
    [('d',3), ('a',2), ('b',3), ('c',1)],
]

expected_medianagg2  = [('c', 1.0), ('a', 3.5), ('b', 4.0), ('d', 5.0)]

class MedianAggregatorTestCases(unittest.TestCase):

    def setUp(self):
        self.mdnragg = ra.MedianRankAggregator()

    def tearDown(self):
        del self.mdnragg

    def test_median_aggregator_1(self):
        assert_equal(self.mdnragg.aggregate(lofls1), expected_medianagg1)

    def test_median_aggregator_2(self):
        assert_equal(self.mdnragg.aggregate(lofls2), expected_medianagg2)


