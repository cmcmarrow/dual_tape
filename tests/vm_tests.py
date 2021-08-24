"""
Copyright 2021 Charles McMarrow
"""

import unittest
# built-in
from typing import List, Optional, Tuple, Union

# dual_tape
from dual_tape.dual_tape import dual_tape_api
from dual_tape.vm import VMState
from .test_files import get_path


def _runner(file: str,
            inputs: Optional[Union[Tuple[str, ...], List[str]]] = None,
            timeout: int = 1000) -> VMState:
    """
    info: Runs VM.
    :param file: str
    :param inputs: Optional[Union[Tuple[str, ...], List[str]]]
    :return: VMState
    """
    if inputs is None:
        inputs = ()
    vm = iter(dual_tape_api(get_path(file), inputs=inputs, sys_output=False, catch_output=True))
    vm_state = next(vm)
    for at, _ in enumerate(vm):
        assert at != timeout
    return vm_state


class VMTests(unittest.TestCase):
    def test_halt(self):
        vm_state = _runner("h.dt")
        self.assertEqual(len(vm_state.output_stream), 0)
        self.assertTrue(vm_state.halt)

    def test_rwon(self):
        vm_state = _runner("rwon.dt")
        stream = vm_state.output_stream
        self.assertEqual(len(stream), 5)
        self.assertEqual(stream[0], "0")
        self.assertEqual(stream[1], "-12345")
        self.assertEqual(stream[2], "45")
        self.assertEqual(stream[3], "122")
        self.assertEqual(stream[4], "0")

    def test_onin(self):
        vm_state = _runner("onin.dt", inputs=("666", "&^*(%(^*", "-404"))
        outputs = vm_state.output_stream
        self.assertEqual(len(outputs), 3)
        self.assertEqual(outputs[0], "666")
        self.assertEqual(outputs[1], "0")
        self.assertEqual(outputs[2], "-404")

    def test_ocic(self):
        vm_state = _runner("ocic.dt", inputs=("cd", "", "a"))
        outputs = vm_state.output_stream
        self.assertEqual(len(outputs), 3)
        self.assertEqual(outputs[0], "c")
        self.assertEqual(outputs[1], "\0")
        self.assertEqual(outputs[2], "a")

    def test_rona(self):
        vm_state = _runner("rona.dt")
        outputs = vm_state.output_stream
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0], "15")

    def test_rons(self):
        vm_state = _runner("rons.dt")
        outputs = vm_state.output_stream
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0], "31")

    def test_rwoc(self):
        vm_state = _runner("rwoc.dt")
        stream = vm_state.output_stream
        self.assertEqual(len(stream), 5)
        self.assertEqual(stream[0], chr(0))
        self.assertEqual(stream[1], "7")
        self.assertEqual(stream[2], "$")
        self.assertEqual(stream[3], "G")
        self.assertEqual(stream[4], chr(0))

    def test_jump(self):
        vm_state = _runner("j.dt")
        self.assertEqual(len(vm_state.output_stream), 0)

    def test_rjd(self):
        vm_state = _runner("rjd.dt")
        self.assertEqual(len(vm_state.output_stream), 0)

    def test_jz(self):
        vm_state = _runner("jz.dt")
        self.assertEqual(len(vm_state.output_stream), 0)

    def test_rjz2(self):
        vm_state = _runner("rjz2.dt")
        self.assertEqual(len(vm_state.output_stream), 0)

    def test_rjg(self):
        vm_state = _runner("rjg.dt")
        self.assertEqual(len(vm_state.output_stream), 0)

    def test_rgz2(self):
        vm_state = _runner("rjg2.dt")
        self.assertEqual(len(vm_state.output_stream), 0)

    def test_ronrd(self):
        pass

    def test_ronwd(self):
        pass

    def test_rrdiwdi(self):
        pass
