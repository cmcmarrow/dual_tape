import argparse
import dual_tape as dt
from . import error
from . import assembler
from . import vm
from . import log


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
                            help="path to dual_tape")
        parser.add_argument("-a",
                            "--author",
                            default=False,
                            action="store_true",
                            help="get author of dual_tape")
        parser.add_argument("-v",
                            "--version",
                            default=False,
                            action="store_true",
                            help="get version of dual_tape")
        parser.add_argument("-l",
                            "--log",
                            default=False,
                            action="store_true",
                            help="enables debug log")
        args = parser.parse_args()

        if args.author:
            print(dt.AUTHOR)

        if args.version:
            print(f"v{dt.MAJOR}.{dt.MINOR}.{dt.MAINTENANCE}")

        dual_tape_api(file=args.file,
                      log=args.log)
    except error.DualTapeError as e:
        print(f"\nERROR: {e}", flush=True)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt!", flush=True)


def dual_tape_api(file: str,
                  log: bool = False) -> None:
    """
    info: API to dual_tape
    :return:
    """
    entry_point, instructions, data = assembler.assembler(file=file)
