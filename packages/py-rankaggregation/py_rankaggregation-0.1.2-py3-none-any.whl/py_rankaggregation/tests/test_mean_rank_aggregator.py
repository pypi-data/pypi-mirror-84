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

expected_meanagg1    = [('a', 2.25), ('b', 3.0), ('c', 3.75), ('d', 4.0)]

# list of lists number 2
lofls2 = [
    [('a',1.2), ('b',.2), ('c',.01)],
    [('a',10), ('b',10), ('c',1)],
    [('d',3), ('a',2), ('b',3), ('c',1)],
]

expected_meanagg2    = [('c', 1.7525), ('d', 4.5), ('a', 4.55), ('b', 4.55)]

class MeanAggregatorTestCases(unittest.TestCase):

    def setUp(self):
        self.mragg = ra.MeanRankAggregator()

    def tearDown(self):
        del self.mragg

    def test_mean_aggregator_1(self):
        assert_equal(self.mragg.aggregate(lofls1), expected_meanagg1)

    def test_mean_aggregator_2(self):
        assert_equal(self.mragg.aggregate(lofls2), expected_meanagg2)


