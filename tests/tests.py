#!/usr/bin/python3

# Some of the test problems for the unrooted case come from an unpublished manuscript whose conference version is
# "Local Problems on Trees from the Perspectives of Distributed Algorithms, Finitary Factors, and Descriptive Combinatorics"
# by Sebastian Brandt, Yi-Jun Chang, Jan Grebík, Christoph Grunau, Václav Rozhoň, and Zoltán Vidnyánszky
# https://arxiv.org/abs/2106.02066
#
# Some of the test problems for the rooted case come from
# "Locally Checkable Problems in Rooted Trees"
# by Alkida Balliu, Sebastian Brandt, Yi-Jun Chang, Dennis Olivetti, Jan Studený, Jukka Suomela, Aleksandr Tereshchenko
# https://arxiv.org/abs/2102.09277

import itertools
import subprocess
import sys
import unittest
from poly_classifier.unrooted_poly_decider import get_new_labels, unrooted_polynomial_classifier
from poly_classifier.rooted_poly_decider import rooted_polynomial_classifier

sqrt_rooted_1 = \
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

sqrt_rooted_2 = \
    b"""a1 : b1 b1
a2 : a1 a1
a2 : a1 b1
a2 : a1 b2
a2 : a1 x1
a2 : b1 b1
a2 : b1 b2
a2 : b1 x1
a2 : b2 b2
a2 : b2 x1
a2 : x1 x1
b1 : a1 a1
b2 : a1 a1
b2 : a1 a2
b2 : a1 b1
b2 : a1 x1
b2 : a2 a2
b2 : a2 b1
b2 : a2 x1
b2 : b1 b1
b2 : b1 x1
b2 : x1 x1
x1 : a1 a1
x1 : a1 a2
x1 : a1 b1
x1 : a1 b2
x1 : a1 x1
x1 : a2 b1
x1 : b1 b1
x1 : b1 b2
x1 : b1 x1

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

unsolvable_trim = \
    b"""A a a
B b b

a a
b b
A b
B c

"""

unsolvable_trim_v2 = \
    b"""A a a
B b b
C c c
D d d
E e e

a a
b b
c c
d d
e e
A b
B c
C d
D e

"""

big_input_v1 = \
    b"""a : b b
a : b c
a : c c
b : a a
b : a c
b : c c
c : a d
c : b d
c : c d
c : d d
d : e e
d : e f
d : f f
e : d d
e : d f
e : f f
f : d g
f : e g
f : f g
f : g g
g : h h
h : g g

"""

big_input_v2 = \
    b"""a : b b
a : b c
a : c c
b : a a
b : a c
b : c c
c : a d
c : b d
c : c d
c : d d
d : e e
d : e f
d : f f
e : d d
e : d f
e : f f
f : d g
f : e g
f : f g
f : g g
g : h h
g : h i
g : i i
h : g g
h : g i
h : i i
i : g j
i : h j
i : i j
i : j j
j : k k
k : j j

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

    def testProblemGenerationUnrooted(self):
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

    def testProblemGenerationRooted(self):
        def create_k_problem(k):
            configurations = []
            def gen(l, s, t):
                return [ f'{l}{j}' for j in range(s, t+1) ]
            for i in range(1, k+1):
                ss = gen('a', 1, i-1) + gen('b', 1, i) + gen('x', 1, i-1)
                for s1 in ss:
                    for s2 in ss:
                        configurations.append([f'a{i}', s1, s2])
            for i in range(1, k+1):
                ss = gen('a', 1, i) + gen('b', 1, i-1) + gen('x', 1, i-1)
                for s1 in ss:
                    for s2 in ss:
                        configurations.append([f'b{i}', s1, s2])
            for i in range(1, k):
                ss1 = gen('a', 1, k) + gen('b', 1, k) + gen('x', 1, k-1)
                ss2 = gen('a', 1, i) + gen('b', 1, i) + gen('x', 1, i-1)
                for s1 in ss1:
                    for s2 in ss2:
                        configurations.append([f'x{i}', s1, s2])
            return configurations

        for i in range(5):
            configurations = create_k_problem(i)
            self.assertEqual(rooted_polynomial_classifier(configurations), i)

    def testSqrtRooted1(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=sqrt_rooted_1, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Problem Π is Θ(n^(1/2)) round solvable.")

    def testSqrtRooted2(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=sqrt_rooted_2, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Problem Π is Θ(n^(1/2)) round solvable.")

    def testThreeCol(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=three_coloring, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Problem Π is O(log(n)) round solvable.")

    def testTwoColWithChoice(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=two_col_with_choice, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Problem Π is O(log(n)) round solvable.")

    def testSinklessOrientation(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=sinkless_orientation, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Problem Π is O(log(n)) round solvable.")

    def testUnsolvableRooted(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=unsolvable_rooted, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Problem Π is 'unsolvable in a strict sense'.")

    def testUnsolvableTrim(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=unsolvable_trim, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Problem Π is 'unsolvable in a strict sense'.")

    def testUnsolvableTrimV2(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=unsolvable_trim_v2, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Problem Π is 'unsolvable in a strict sense'.")

    def testBigInputV1(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=big_input_v1, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Problem Π is Θ(n^(1/2)) round solvable.")

    def testBigInputV2(self):
        result = subprocess.run([sys.executable, '-m', 'poly_classifier'], input=big_input_v2, capture_output=True)
        lines = str(result.stdout.decode('utf-8')).split('\n')
        self.assertEqual(lines[-2], "Problem Π is Θ(n^(1/2)) round solvable.")

