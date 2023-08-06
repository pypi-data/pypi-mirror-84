# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json

from setuptools import find_packages, setup


with open("requirements.json") as json_file:
    data = json.load(json_file)
    requirements = data["sapp"]

setup(
    name="fb-sapp",
    version="0.2.2",
    install_requires=requirements,
    entry_points={"console_scripts": ["sapp = sapp.cli:cli"]},
    packages=find_packages(),
    url="https://pyre-check.org/",
    author="Facebook",
    maintainer_email="pyre@fb.com",
)
