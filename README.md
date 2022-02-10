
## Description

This folder contains a program that decides round complexity of homogenous LCL problems on (binary) trees in the polynomial region.

## Usage

1. Install dependencies by `pip3 install -r requirements.txt`.

2. Run `python -m poly_classifier` and describe (on standard input) configurations of a problem.
For example:

_Note that one needs to first run the classifier (`python -m poly_classifier`) and only afterwards provide an input
on a separate lines._

```
> python -m poly_classifier 
Polynomial classifier for homogenous trees (currently for binary rooted & unrooted trees)
For unrooted case, use node configuration in form: 'A B C' and edge configurations in form 'A B'
For rooted case, use only node configurations in form 'A: B C'.
Node configurations: (each configuration on a new line and end with empty line)
a a a
b b b

Edge configurations: (each configuration on a new line and end with empty line)
a b

Complexity of the problem is Θ(n^(1/1)).

```
## Tests

To execute tests, run the following from the root directory:

```
python -m unittest discover
```
