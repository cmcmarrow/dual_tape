"""
Copyright 2021 Charles McMarrow

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# built-in
import setuptools
from distutils.core import setup
import os


# dual_tape
import dual_tape


with open(os.path.join("README.rst")) as readme:
    long_description = readme.read()

setup(
    name="dual_tape",
    version=f"{dual_tape.MAJOR}.{dual_tape.MINOR}.{dual_tape.MAINTENANCE}",
    author=dual_tape.AUTHOR,
    author_email="Charles.McMarrow.4@gmail.com",
    url="https://github.com/cmcmarrow/dual_tape",
    license="Apache Software License 2.0",
    description="Tape Esolang",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=["dual_tape"],

    extras_require={"dev": ["wheel", "twine", "pyinstaller"]},

    classifiers=["Development Status :: 6 - Mature",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "Natural Language :: English",
                 "Operating System :: Microsoft :: Windows",
                 "Operating System :: POSIX :: Linux",
                 "Operating System :: MacOS :: MacOS X",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10"],

    entry_points={"console_scripts": ["dual_tape = dual_tape.dual_tape:dual_tape"]}
)
