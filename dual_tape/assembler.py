"""
Copyright 2021 Charles McMarrow
"""


from typing import Dict, Tuple
from .error import DualTapeError
from .vm import INSTRUCTIONS


class AssemblerError(DualTapeError):
    @classmethod
    def name_collection(cls, name: str):
        """
        info: Indicates that a name is used more than once.
        :param name: str
        :return: AssemblerError
        """
        return cls(f"Name {repr(name)} can't be used more than once!")

    @classmethod
    def missing_name(cls, name: str):
        """
        info: Indicates that a name can't be found.
        :param name: str
        :return: AssemblerError
        """
        return cls(f"Name {repr(name)} can't be found!")

    @classmethod
    def bad_line(cls, line: str, at: int):
        """
        info: Indicates that a line is not valid.
        :param line: str
        :param at: int
        :return: AssemblerError
        """
        return cls(f"Bad line {at}: {repr(line)}!")

    @classmethod
    def missing_entry_point(cls):
        """
        info: Indicates that the program is missing an entry point.
        :return: AssemblerError
        """
        return cls("Program does not have an entry point!")

    @classmethod
    def file_not_found(cls, file: str):
        """
        info: Indicates that the program can't be found.
        :param: file: str
        :return: AssemblerError
        """
        return cls(f"File {repr(file)} cant be found!")


def _read_file(file: str):
    try:
        with open(file) as handler:
            for raw_line in handler:
                line = raw_line.rstrip("\n").split()
                yield [part for part in line if part], raw_line.rstrip("\n")
    except FileNotFoundError:
        raise AssemblerError.file_not_found(file)


def assembler(file: str) -> Tuple[int, Dict[int, int], Dict[int, int]]:
    """
    info: Takes a program and converts it into machine code.
    :param file: str
    :return: Tuple[Dict[int, int], Dict[int, int]]
    """
    instructions, data = {}, {}
    name_space = {}
    at = 0
    for parts, _ in _read_file(file):
        if parts and not parts[0].startswith("#"):
            if parts[0].startswith("@"):
                name = parts[0][1:]
                if name in name_space:
                    raise AssemblerError.name_collection(name)
                name_space[name] = at
            at += 1
    at = 0
    for line_number, line_data in enumerate(_read_file(file)):
        parts, line = line_data
        if parts and not parts[0].startswith("#"):
            if parts[0].startswith("@"):
                del parts[0]
            try:
                if len(parts[0]) != 1 or ord(parts[0]) not in INSTRUCTIONS:
                    raise AssemblerError.bad_line(line, line_number + 1)
                instructions[at] = ord(parts.pop(0))
                if parts and not parts[0].startswith("#"):
                    try:
                        data[at] = int(parts[0])
                        del parts[0]
                    except ValueError:
                        if parts[0].startswith("@"):
                            name = parts.pop(0)[1:]
                            if name not in name_space:
                                raise AssemblerError.missing_name(name)
                            data[at] = name_space[name]
                        elif parts[0].startswith("c") and len(parts[0]) == 2:
                            data[at] = ord(parts.pop(0)[1])
                        else:
                            raise AssemblerError.bad_line(line, line_number + 1)
                    if parts and not parts[0].startswith("#"):
                        raise AssemblerError.bad_line(line, line_number + 1)
            except IndexError:
                raise AssemblerError.bad_line(line, line_number + 1)
            at += 1
    entry_point = name_space.get("")
    if entry_point is None:
        raise AssemblerError.missing_entry_point()
    return entry_point, instructions, data
