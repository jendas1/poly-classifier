#!/bin/bash

# build
python3 setup.py sdist bdist_wheel

# check
twine check dist/*

# publish
twine upload dist/*

# cleanup
rm -rf ./build
rm -rf ./dist
rm -rf ./poly-classifier.egg-info
