import itertools
import math

try:
    from .rooted_poly_decider import rooted_polynomial_classifier
    from .unrooted_poly_decider import unrooted_polynomial_classifier
except ImportError:
    from poly_classifier import rooted_polynomial_classifier
    from poly_classifier import unrooted_polynomial_classifier

if __name__ == "__main__":
    print(
        "Polynomial classifier for homogenous trees (currently for binary rooted & unrooted trees)"
    )
    print(
        "For unrooted case, use node configuration in form: 'A B C' and edge configurations in form 'A B'"
    )
    print("For rooted case, use only node configurations in form 'A: B C'.")
    configurations = []
    k = None
    line = input(
        "Node configurations: (each configuration on a new line and end with empty line)\n"
    )
    if ":" in line:  # rooted case
        while line != "":
            configurations.append(
                tuple(
                    itertools.chain(
                        *[x.split() for x in line.strip().split(":")])))
            line = input()
        k = rooted_polynomial_classifier(configurations)
    else:  # unrooted case
        while line != "":
            configurations.append(tuple(line.split()))
            line = input()
        edge_configurations = []
        line = input(
            "Edge configurations: (each configuration on a new line and end with empty line)\n"
        )
        while line != "":
            edge_configurations.append(tuple(line.split()))
            line = input()
        k = unrooted_polynomial_classifier(configurations, edge_configurations)
    if k == 0:
        print(f"Problem Π is 'unsolvable in a strict sense'.")
    elif k == math.inf:
        print(f"Problem Π is O(log(n)) round solvable.")
    else:
        print(f"Problem Π is Θ(n^(1/{k})) round solvable.")
