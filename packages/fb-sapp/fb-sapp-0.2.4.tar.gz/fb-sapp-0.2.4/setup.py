# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json

from pathlib import Path
from setuptools import find_packages, setup


with open("requirements.json") as json_file:
    data = json.load(json_file)
    requirements = data["sapp"]

setup(
    name="fb-sapp",
    version="0.2.4",
    description="Static Analysis Post-Processor for processing taint analysis results.",
    long_description=Path('README.md').read_text(),
    install_requires=requirements,
    entry_points={"console_scripts": ["sapp = sapp.cli:cli"]},
    packages=find_packages(),
    url="https://pyre-check.org/",
    author="Facebook",
    maintainer_email="pyre@fb.com",
)
