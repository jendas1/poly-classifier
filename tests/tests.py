#!/usr/bin/python3

# Test problems for the unrooted case come from an unpublished manuscript whose conference version is named:
# Local Problems on Trees from the Perspectives of Distributed Algorithms, Finitary Factors, and Descriptive Combinatorics
# by Brandt, Sebastian ; Chang, Yi-Jun ; Grebík, Jan ; Grunau, Christoph ; Rozhoň, Václav ; Vidnyánszky, Zoltán

import itertools
import subprocess
import sys
import unittest
from poly_classifier.unrooted_poly_decider import get_new_labels, unrooted_polynomial_classifier

sqrt_input = \
    b"""1 : 2 2
1 : 2 x
1 : x x
2 : 1 1
2 : 1 x
2 : x x
x : 1 a
x : 2 a
x : x a
x : a a
a : b b
b : a a

"""

three_coloring = \
    b"""1 1 1
2 2 2
3 3 3

1 2
1 3
2 3

"""

two_col_with_choice = \
    b"""a: a b
b: a a

"""

sinkless_orientation = \
    b"""a b b
a a b
a a a

a b

"""

unsolvable_rooted = \
    b"""a: a b
b: b c
c: c d
d: d e

"""

class TestE2E(unittest.TestCase):
    def testPolyDecider(self):
        result = get_new_labels([('A', 'A', 'A')], [('A', 'A')], ['A'])
        self.assertEqual(result, set('A'))

    def testTwoCol(self):
        self.assertEqual(unrooted_polynomial_classifier([(1, 1, 1), (2, 2, 2)], [(1, 2)]), 1)

    def testSqrtProb(self):
        C2 = [("x1", "x1", "y1"), ("x2", "x2", "y2")]
        R2 = [("a1", "b1", "b1"), ("a2", "b2", "b2")]
        RS2 = [("b1", "b1", "b1"), ("b2", "b2", "b2")]

        V2 = list(itertools.chain(C2, R2, RS2))

        E2 = [("a1", "a1"), ("a2", "a2"), ("x1", "x1"), ("x2", "x2"),
              ("x1", "b2"), ("x1", "y2"),
              ("a1", "b1"), ("a1", "b2"), ("a1", "y1"), ("a2", "b2")]

        self.assertEqual(unrooted_polynomial_classifier(V2, E2), 2)  # 2 (rake & compress)

    def testProblemGeneration(self):
        def create_k_problem(k):


            comp_confs = [(f"x{i}", f"x{i}", f"y{i}") for i in range(k)]
            rake_confs = [(f"a{i}", f"b{i}", f"b{i}") for i in range(k)]
            rake_star_confs = [(f"b{i}", f"b{i}", f"b{i}") for i in range(k)]

            configurations = list(itertools.chain(comp_confs, rake_confs, rake_star_confs))

            edge_confs_1 = [(f"a{i}", f"a{i}") for i in range(k)] + [(f"x{i}", f"x{i}") for i in range(k)]
            edge_confs_2 = [(f"x{i}", f"b{j}") for j in range(k) for i in range(k) if i < j] + \
                           [(f"x{i}", f"y{j}") for j in range(k) for i in range(k) if i < j]
            edge_confs_3 = [(f"a{i}", f"b{j}") for j in range(k) for i in range(k) if i <= j] + \
                           [(f"a{i}", f"y{j}") for j in range(k) for i in range(k) if i <= j]
            edge_configurations = list(itertools.chain(edge_confs_1, edge_confs_2, edge_confs_3))
            return configurations, edge_configurations

        for i in range(5):
            configurations, edge_configurations = create_k_problem(i)
            self.assertEqual(unrooted_polynomial_classifier(configurations, edge_configurations), i)

    def testSqrtProbRooted(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=sqrt_input, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Complexity of the problem is Θ(n^(1/2)).")

    def testThreeCol(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=three_coloring, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Complexity of the problem is Θ(n^(1/inf)).")

    def testTwoColWithChoice(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=two_col_with_choice, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Complexity of the problem is Θ(n^(1/inf)).")

    def testSinklessOrientation(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=sinkless_orientation, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Complexity of the problem is Θ(n^(1/inf)).")

    def testUnsolvableRooted(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=unsolvable_rooted, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Complexity of the problem is Θ(n^(1/0)).")
