# assumptions: Δ = 3
# configurations = [(root,child_1,child_2),...] (node configurations)
# edge_configurations = [(half_1,half_2),...] (edge configuraitons)
# labels = set([label_1,label_2,...])
import itertools
import math

from networkx.utils.union_find import UnionFind
from rooted_tree_classifier.log_decider import isFlexible

delta = 3


def get_labels(configurations):
    labels = set()
    for conf in configurations:
        for label in conf:
            labels.add(label)
    return labels


def trim(configurations, edge_configurations):
    # trim outputs a subset of configurations that can label any sufficiently large Δ-regular tree
    # lemma 4.24 in the paper
    labels = get_labels(configurations)
    while True:
        new_labels = get_new_labels(configurations, edge_configurations,
                                    labels)
        assert not (set(new_labels) - set(labels))
        if set(new_labels) == set(labels):
            break
        else:
            labels = new_labels
    # trim configurations
    trimmed_configurations = []
    for conf in configurations:
        ok = True
        for first_label in conf:
            found = False
            for sec_label in labels:
                if (first_label, sec_label) in edge_configurations or \
                        (sec_label, first_label) in edge_configurations:
                    found = True
            if not found:
                ok = False
                break
        if ok:
            trimmed_configurations.append(conf)
    return trimmed_configurations


def get_new_labels(configurations, edge_configurations, old_labels):
    new_labels = set()
    for conf in configurations:
        for i in range(delta):
            pot_label = conf[i]
            ok = True
            for j in range(delta):
                first_label = conf[j]
                if i == j:
                    continue
                found = False
                for sec_label in old_labels:
                    if (first_label, sec_label) in edge_configurations or \
                            (sec_label, first_label) in edge_configurations:
                        found = True
                if not found:
                    ok = False
                    break
            if ok:
                new_labels.add(pot_label)
    return new_labels


def create_graph(configurations, edge_configurations):
    path_configurations = set(
        itertools.chain(
            *[itertools.permutations(conf, 2) for conf in configurations]))
    graph = {path_conf: [] for path_conf in path_configurations}
    for s, edges in graph.items():
        for t in graph.keys():
            if (s[1], t[0]) in edge_configurations or \
                    (t[0], s[1]) in edge_configurations:
                edges.append(t)
    return graph


def is_reachable(graph, s, t, vis=None):
    if vis is None:
        vis = set()
    if s not in vis:
        vis.add(s)
        for c in graph[s]:
            if c == t:
                return True
            if is_reachable(graph, c, t, vis):
                return True
        return False


def restrict(configurations, multisets):
    restricted = []
    for conf in configurations:
        ok = True
        for permutation in itertools.permutations(conf, 2):
            if not permutation in multisets:
                ok = False
                break
        if ok:
            restricted.append(conf)
    return restricted


def flexible_scc_restrictions(configurations, edge_configurations):
    # output: list of all restrictions
    # lemma 4.25 in the paper

    # create automaton M
    graph = create_graph(configurations, edge_configurations)
    # find all strongly connected component (as defined in Definition 4.4)
    components = UnionFind()
    for s in graph.keys():
        for t in graph.keys():
            if (is_reachable(graph, s, t)
                    and is_reachable(graph, s, (t[1], t[0]))
                    and is_reachable(graph, (s[1], s[0]), t)
                    and is_reachable(graph, (s[1], s[0]), (t[1], t[0]))):
                components.union(s, t)

    flexible_restrictions = []
    # for each component check if it is path-flexible
    # if yes, add it to flexible restrictions
    for component in components.to_sets():
        representative = list(component)[0]
        if isFlexible(graph, representative):
            flexible_restrictions.append(restrict(configurations, component))
    return flexible_restrictions


def max_depth(configurations, edge_configurations):
    if not configurations:
        return 0
    maximum = 0
    for flexible_restriction in flexible_scc_restrictions(
            configurations, edge_configurations):
        if set(configurations) - set(
                flexible_restriction):  # if we removed something
            depth = max_depth(trim(flexible_restriction, edge_configurations),
                              edge_configurations)
            maximum = max(maximum, depth)
        else:
            return math.inf
    return 1 + maximum


def unrooted_polynomial_classifier(configurations, edge_configurations):
    return max_depth(trim(configurations, edge_configurations),
                     edge_configurations)
