import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="poly-classifier",
    version="0.0.1",
    description=
    "A command-line tool for automatically classifying LCL problems on regular trees in the polynomial region.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="Unlicense",
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["poly_classifier"],
    include_package_data=True,
    install_requires=["rooted_tree_classifier", "networkx"])
