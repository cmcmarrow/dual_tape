"""
Copyright 2021 Charles McMarrow
"""

# built-in
from dataclasses import dataclass
from typing import Callable, Dict, List, Generator, Optional, Tuple, Union

# dual_tape
from . import log


@dataclass
class VMState:
    pc: int
    instructions: Dict[int, int]
    data: Dict[int, int]
    inputs: Optional[Union[Tuple[str, ...], List[str]]]
    sys_output: bool
    output_stream: Optional[List[str]]
    operations: List[Callable[["VMState"], None]]
    halt: bool = False
    item1: int = 0
    item2: int = 0


def _read_instruction(vm_state: VMState, pc: Optional[int] = None) -> int:
    """
    info: Gets an instruction.
    :param vm_state: VMState
    :param pc: Optional[int]
    :return: int
    """
    if pc is None:
        pc = vm_state.pc
    return vm_state.instructions.get(pc, ord("n"))


def _read_memory(vm_state: VMState, pc: Optional[int] = None) -> int:
    """
    info: Gets an data from memory.
    :param vm_state: VMState
    :param pc: Optional[int]
    :return: int
    """
    if pc is None:
        pc = vm_state.pc
    return vm_state.data.get(pc, 0)


def _out(vmstate: VMState, data: str) -> None:
    """
    info: Writes output to console.
    :param vmstate: VMState
    :param data: str
    :return: None
    """
    if vmstate.sys_output:
        print(data, flush=True, end="")

    if vmstate.output_stream is not None:
        vmstate.output_stream.append(data)


def _in(vmstate: VMState) -> str:
    """
    info: Gets input from user.
    :param vmstate: VMState
    :return: str
    """
    if vmstate.inputs is not None:
        if vmstate.inputs:
            return vmstate.inputs.pop(0)
        return ""
    return input()


def next_instruction(vmstate: VMState) -> None:
    """
    info: Will slide to the next operation.
    :param vmstate: VMState
    :return: None
    """
    vmstate.operations.append(vmstate.operations.pop(0))
    log.log(f"Next: {vmstate.operations[0].__name__}")
    vmstate.pc += 1


def execute(vmstate: VMState) -> None:
    """
    info: Will execute selected operation.
    :param vmstate: VMState
    :return: None
    """
    log.log(f"EXECUTE: {vmstate.operations[0].__name__}!!!")
    vmstate.operations[0](vmstate)


def halt(vmstate: VMState) -> None:
    """
    info: Will halt the program.
    :param vmstate: VMState
    :return: None
    """
    vmstate.halt = True
    vmstate.pc += 1


def out_number(vmstate: VMState) -> None:
    """
    info: Will echo number to console.
    :param vmstate: VMState
    :return: None
    """
    _out(vmstate, str(vmstate.item1))
    vmstate.pc += 1


def out_character(vmstate: VMState) -> None:
    """
    info: Will echo a character to console.
    :param vmstate: VMState
    :return: None
    """
    try:
        _out(vmstate, chr(vmstate.item1))
    except (OverflowError, ValueError):
        log.log(f"{vmstate.item1} does not map to a character!")
    vmstate.pc += 1


def in_number(vmstate: VMState) -> None:
    """
    info: Get number from user.
    :param vmstate: VMState
    :return: None
    """
    vmstate.item2 = vmstate.item1
    try:
        vmstate.item1 = int(_in(vmstate))
    except ValueError:
        vmstate.item1 = 0
    vmstate.pc += 1


def in_character(vmstate: VMState) -> None:
    """
    info: Get character from user.
    :param vmstate: VMState
    :return: None
    """
    vmstate.item2 = vmstate.item1
    try:
        vmstate.item1 = ord(_in(vmstate)[0])
    except IndexError:
        vmstate.item1 = 0
    vmstate.pc += 1


def add(vmstate: VMState) -> None:
    """
    info: Add two number together.
    :param vmstate: VMState
    :return: None
    """
    vmstate.item1 = vmstate.item2 + vmstate.item1
    vmstate.pc += 1


def subtract(vmstate: VMState) -> None:
    """
    info: Subtract to numbers together.
    :param vmstate: VMState
    :return: None
    """
    vmstate.item1 = vmstate.item2 + vmstate.item1
    vmstate.pc += 1


def jump(vmstate: VMState) -> None:
    """
    info: Jump to location.
    :param vmstate: VMState
    :return: None
    """
    vmstate.pc = _read_memory(vmstate)


def jump_dynamic(vmstate: VMState) -> None:
    """
    info: Jump to location dynamically.
    :param vmstate: VMState
    :return: None
    """
    vmstate.pc = vmstate.item1


def jump_zero(vmstate: VMState) -> None:
    """
    info: Jump to location dynamically if zero.
    :param vmstate: VMState
    :return: None
    """
    if not vmstate.item2:
        vmstate.pc = vmstate.item1
    else:
        vmstate.pc += 1


def jump_greater(vmstate: VMState) -> None:
    """
    info: Jump to location dynamically if greater than zero.
    :param vmstate: VMState
    :return: None
    """
    if vmstate.item2 > 0:
        vmstate.pc = vmstate.item1
    else:
        vmstate.pc += 1


def read(vmstate: VMState) -> None:
    """
    info: Read data.
    :param vmstate: VMState
    :return: None
    """
    vmstate.item2 = vmstate.item1
    vmstate.item1 = _read_memory(vmstate)
    vmstate.pc += 1


def read_dynamic(vmstate: VMState) -> None:
    """
    info: Read data dynamically.
    :param vmstate: VMState
    :return: None
    """
    vmstate.item2 = vmstate.item1
    vmstate.item1 = _read_memory(vmstate, vmstate.item2)
    vmstate.pc += 1


def read_dynamic_instruction(vmstate: VMState) -> None:
    """
    info: Read instruction dynamically.
    :param vmstate: VMState
    :return: None
    """
    vmstate.item2 = vmstate.item1
    vmstate.item1 = _read_instruction(vmstate, vmstate.item2)
    vmstate.pc += 1


def write(vmstate: VMState) -> None:
    """
    info: Write data.
    :param vmstate: VMState
    :return: None
    """
    vmstate.data[vmstate.pc] = vmstate.item1
    vmstate.pc += 1


def write_dynamic(vmstate: VMState) -> None:
    """
    info: Write data dynamically.
    :param vmstate: VMState
    :return: None
    """
    vmstate.data[vmstate.item1] = vmstate.item2
    vmstate.pc += 1


def write_dynamic_instruction(vmstate: VMState) -> None:
    """
    info: Write instruction dynamically.
    :param vmstate: VMState
    :return: None
    """
    if vmstate.item2 in INSTRUCTIONS:
        vmstate.instructions[vmstate.item1] = vmstate.item2
    vmstate.pc += 1


INSTRUCTIONS: Dict[int, Callable[[VMState], None]] = {ord("n"): next_instruction,
                                                      ord("x"): execute}


def vm(entry_point: int,
       instructions: Dict[int, int],
       data: Dict[int, int],
       inputs: Optional[Union[Tuple[str, ...], List[str]]],
       sys_output: bool,
       catch_output: bool) -> Generator[VMState, None, None]:
    """
    info: VM for dual_tape.
    :param entry_point: int
    :param instructions: Dict[int, int]
    :param data: Dict[int, int]
    :param inputs: Optional[Union[Tuple[str, ...], List[str]]]
    :param sys_output: bool
    :param catch_output: bool
    :return: Generator[VMState, None, None]
    """

    if isinstance(inputs, tuple):
        inputs = list(inputs)

    output_stream = None
    if catch_output:
        output_stream = []

    vm_state = VMState(entry_point,
                       instructions,
                       data,
                       inputs,
                       sys_output,
                       output_stream,
                       [halt,
                        out_number,
                        out_character,
                        in_number,
                        in_character,
                        add,
                        subtract,
                        jump,
                        jump_dynamic,
                        jump_zero,
                        jump_greater,
                        read,
                        read_dynamic,
                        read_dynamic_instruction,
                        write,
                        write_dynamic,
                        write_dynamic_instruction])
    yield vm_state
    while not vm_state.halt:
        log.log("PC: {}, I: {}, M: {}, i: {}, i2: {}".format(vm_state.pc,
                                                             _read_instruction(vm_state),
                                                             _read_memory(vm_state),
                                                             vm_state.item1,
                                                             vm_state.item2))
        instruction = INSTRUCTIONS[_read_instruction(vm_state)]
        instruction(vm_state)
        yield vm_state
