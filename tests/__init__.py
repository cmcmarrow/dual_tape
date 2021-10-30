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

Holds tests for dual_tape.
"""

# built-in
import inspect
import sys
import unittest

# dual_tape
from . import assembler_tests
from . import vm_tests

# add all tests to namespace
for module_name, module in vars().copy().items():
    if inspect.ismodule(module) and module_name != "unittest":
        for module_var_name, module_var in vars(module).items():
            if inspect.isclass(module_var) and unittest.TestCase in module_var.__mro__:
                assert not hasattr(sys.modules[__name__], module_var_name)
                setattr(sys.modules[__name__], module_var_name, module_var)
            del module_var_name
            del module_var
    del module_name
    del module


def tests() -> None:
    """
    info: Run tests and write to stdio.
    :return: None
    """
    unittest.main(module=__name__,
                  exit=False)
