#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="py-gql-client",
    version="0.0.3",
    author="Facebook Inc.",
    description="Python GraphQL generated code client",
    packages=setuptools.find_packages(include=["gql_client*"]),
    classifiers=["Programming Language :: Python :: 3.7"],
    python_requires=">=3.7",
    include_package_data=True,
    scripts=["bin/gql-compiler"],
    install_requires=[
        "graphql-core>=3",
        "unicodecsv>=0.14.1",
        "requests>=2.22.0",
        "dataclasses-json==0.3.2",
    ],
)
