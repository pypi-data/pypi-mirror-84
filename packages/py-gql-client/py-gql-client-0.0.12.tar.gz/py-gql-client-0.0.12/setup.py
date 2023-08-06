#!/usr/bin/env python3

import setuptools
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
long_description = ""
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="py-gql-client",
    version="0.0.12",
    author="Facebook Inc.",
    description="Python GraphQL generated code client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=["gql_client", "gql_client.*"]),
    license="BSD License",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    scripts=["bin/gql-compiler"],
    install_requires=[
        "graphql-core>=3",
        "gql>=v3.0.0a4",
        "unicodecsv>=0.14.1",
        "requests>=2.22.0",
        "dataclasses-json==0.3.2",
    ],
)
