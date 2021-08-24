"""
Copyright 2021 Charles McMarrow
"""

# built-in
import argparse
from typing import List, Generator, Optional, Tuple, Union

# dual_tape
import dual_tape as dt
from . import assembler
from . import error
from . import vm
from .log import enable_log


class DualTapeAPI(error.DualTapeError):
    @classmethod
    def hit_timeout(cls):
        return cls("Hit timeout!")


def dual_tape() -> None:
    """
    info: Console Interface into dual_tape.
    :return: None
    """
    try:
        parser = argparse.ArgumentParser(description="dual_tape")
        parser.add_argument("file",
                            type=str,
                            action="store",
                            help="path to dual_tape script")
        parser.add_argument("-a",
                            "--author",
                            default=False,
                            action="store_true",
                            help="get author of dual_tape")
        parser.add_argument("-l",
                            "--log",
                            default=False,
                            action="store_true",
                            help="enables debug log")
        parser.add_argument("-v",
                            "--version",
                            default=False,
                            action="store_true",
                            help="get version of dual_tape")
        parser.add_argument("--timeout",
                            default=-1,
                            type=int,
                            help="max number of instructions that can run")
        args = parser.parse_args()

        if args.author:
            print(dt.AUTHOR)

        if args.version:
            print(f"v{dt.MAJOR}.{dt.MINOR}.{dt.MAINTENANCE}")

        for at, _ in enumerate(dual_tape_api(file=args.file, log=args.log)):
            if at == args.timeout:
                raise DualTapeAPI.hit_timeout()

    except error.DualTapeError as e:
        print(f"\nERROR: {e}", flush=True)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt!", flush=True)


def dual_tape_api(file: str,
                  inputs: Optional[Union[Tuple[str, ...], List[str]]] = None,
                  sys_output: bool = True,
                  catch_output: bool = False,
                  log: bool = False) -> Generator[vm.VMState, None, None]:
    """
    info: API to dual_tape
    :param: inputs: Optional[Union[Tuple[str, ...], List[str]]]
    :param: sys_output: bool
    :param: catch_output: bool
    :param: log: bool
    :return: Generator[vm.VMState, None, None]
    """
    if log:
        enable_log()
    entry_point, instructions, data = assembler.assembler(file=file)
    return vm.vm(entry_point, instructions, data, inputs, sys_output, catch_output)
