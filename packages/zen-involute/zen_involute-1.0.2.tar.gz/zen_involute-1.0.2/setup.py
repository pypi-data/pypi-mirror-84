#!/usr/bin/env python3
# coding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zen_involute",
    version="1.0.2",
    author="Mark Zorikhin",
    author_email="hnau256@gmail.com",
    description="Involute gear profile builder for ZenCAD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hnau_zen/involute",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)