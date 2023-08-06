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

expected_geomeanagg1 = [('a', 1.7782794100389228),
  ('b', 2.7831576837137404),
  ('d', 3.3437015248821096),
  ('c', 3.6628415014847064)]

# list of lists number 2
lofls2 = [
    [('a',1.2), ('b',.2), ('c',.01)],
    [('a',10), ('b',10), ('c',1)],
    [('d',3), ('a',2), ('b',3), ('c',1)],
]

expected_geomeanagg2 = [('c', 0.47287080450158797),
  ('b', 2.340347319320716),
  ('a', 3.309750919646873),
  ('d', 4.400558683966967)]

class GeometricMeanAggregatorTestCases(unittest.TestCase):

    def setUp(self):
        self.gmragg = ra.GeometricMeanRankAggregator()

    def tearDown(self):
        del self.gmragg

    def test_geomean_aggregator_1(self):
        assert_equal(self.gmragg.aggregate(lofls1), expected_geomeanagg1)

    def test_geomean_aggregator_2(self):
        assert_equal(self.gmragg.aggregate(lofls2), expected_geomeanagg2)


