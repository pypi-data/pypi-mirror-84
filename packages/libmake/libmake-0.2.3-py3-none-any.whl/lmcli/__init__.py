import sys
import argparse
import pathlib
import subprocess


def pymake():
    # allow for passing filepath
    parser = argparse.ArgumentParser(
        description="Run 'makefile.py' (and pass arguments to it)"
    )
    parser.add_argument("args", nargs="*", help="targets for 'makefile.py'")
    parser.add_argument(
        "-f",
        "--file",
        default="makefile.py",
        type=pathlib.Path,
        help="file path for 'makefile.py' like script",
    )
    args_ns = parser.parse_args()
    makefile = args_ns.file.absolute()

    if makefile.is_file():
        subprocess.run(["python3", str(makefile)] + args_ns.args)
    else:
        here = pathlib.Path(".")
        raise ValueError(
            f"'pymake' needs a valid 'makefile.py', no one found at:\n\t {here.absolute()}"
        )
