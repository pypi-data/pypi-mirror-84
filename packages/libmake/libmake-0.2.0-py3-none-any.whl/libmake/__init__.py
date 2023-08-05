import argparse

from .makefile import Makefile


def run_make(makefile):
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="*")
    args = ap.parse_args()
    makefile.run(args.targets)
