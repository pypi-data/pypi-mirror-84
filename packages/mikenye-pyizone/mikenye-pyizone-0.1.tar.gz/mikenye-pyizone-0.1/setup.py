#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mikenye-pyizone", # Replace with your own username
    version="0.1",
    author="Mike Nye",
    description="Query and control of WiFi-enabled iZone 310 and compatible family of climate control devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikenye/pyizone",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Topic :: Home Automation",
    ],
    python_requires='>=3.5',
)
