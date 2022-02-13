# assumptions: δ = 2
# configurations = [(root,child_1,child_2),...]
# labels = set([label_1,label_2,...])
import math

import networkx
from rooted_tree_classifier.log_decider import isFlexible


def get_labels(configurations):
    labels = set()
    for conf in configurations:
        for label in conf:
            labels.add(label)
    return labels


def trim(labels, configurations):
    # trim outputs a subset of labels that can label any sufficiently large Δ-regular tree
    # lemma 5.28 in the paper
    while True:
        new_labels = get_new_labels(labels, configurations)
        assert not (set(new_labels) - set(labels)
                    )  # trimming labels should not introduce any new labels
        if set(new_labels) == set(labels):
            break
        else:
            labels = new_labels
    return labels


def get_new_labels(old_labels, configurations):
    new_labels = set()
    for conf in configurations:
        pot_label = conf[0]
        if pot_label not in old_labels:
            continue
        ok = True
        for cont_label in conf[1:]:
            if cont_label not in old_labels:
                ok = False
                break
        if ok:
            new_labels.add(pot_label)
    return new_labels


def create_graph(labels, configurations):
    graph = {label: [] for label in labels}
    for conf in configurations:
        head = conf[0]
        if head in labels:
            for tail in conf[1:]:
                if tail in labels:
                    graph[head].append(tail)
    return graph


def flexible_scc_restrictions(labels, configurations):
    # output: list of all label restrictions
    # lemma 5.29 in the paper

    # create automaton M
    graph = create_graph(labels, configurations)
    # find all strongly connected component
    nxgraph = networkx.to_networkx_graph(graph, create_using=networkx.DiGraph)
    flexible_restrictions = []
    for component in networkx.strongly_connected_components(nxgraph):
        representative = list(component)[0]
        if isFlexible(graph, representative):
            flexible_restrictions.append(component)
    return flexible_restrictions


def max_depth(labels, configurations):
    if not labels:
        return 0
    maximum = 0
    for flexible_restriction in flexible_scc_restrictions(
            labels, configurations):
        if labels - flexible_restriction:  # if we removed something
            depth = max_depth(trim(flexible_restriction, configurations),
                              configurations)
            maximum = max(maximum, depth)
        else:
            return math.inf
    return 1 + maximum


def rooted_polynomial_classifier(configurations):
    labels = get_labels(configurations)
    return max_depth(trim(labels, configurations), configurations)
