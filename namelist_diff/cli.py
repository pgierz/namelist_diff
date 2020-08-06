"""Console script for namelist_diff."""
import argparse
import sys
import tempfile
from itertools import zip_longest

import dictdiffer
import f90nml

from .namelist_diff import (
    ansi_ljust,
    clean_mvstreamctl,
    clean_paths,
    clean_set_stream,
    clean_set_stream_element,
    format_nml,
    longest_line_global,
)


def main():
    """Console script for namelist_diff."""
    parser = argparse.ArgumentParser()
    parser.add_argument("nml1")
    parser.add_argument("nml2")
    parser.add_argument("--keep_mvstreamctl", action="store_true")
    parser.add_argument("--keep_set_stream", action="store_true")
    parser.add_argument("--keep_set_stream_element", action="store_true")
    parser.add_argument("--raw_paths", action="store_true")
    args = parser.parse_args()

    print("Comparison for namelists")
    print("------------------------")
    print(f"1st namelist \t {args.nml1}")
    print(f"2nd namelist \t {args.nml2}")

    nml1 = f90nml.read(args.nml1)
    nml2 = f90nml.read(args.nml2)

    for cleanup_func in [
        clean_set_stream_element,
        clean_mvstreamctl,
        clean_paths,
        clean_set_stream,
    ]:
        nml1 = cleanup_func(nml1)
        nml2 = cleanup_func(nml2)

    diff = dictdiffer.diff(nml1, nml2, expand=True)
    diff_swap = dictdiffer.swap(dictdiffer.diff(nml1, nml2, expand=True))

    f1 = tempfile.NamedTemporaryFile(mode="w+")
    f2 = tempfile.NamedTemporaryFile(mode="w+")

    # f1 = open("nml_diff1", mode="w+")
    # f2 = open("nml_diff2", mode="w+")

    print("Formatting nml1...")
    format_nml(nml1, f1, diff)
    print("Formatting nml2...")
    format_nml(nml2, f2, diff_swap)

    f1.flush()
    f2.flush()

    f1.seek(0)
    f2.seek(0)

    # nml1_human_readable = open(args.nml1).read().split("\n")
    # nml2_human_readable = open(args.nml2).read().split("\n")
    nml1_human_readable = f1.read().split("\n")

    nml1_human_readable = [fr"{item}" for item in nml1_human_readable]
    # nml2_human_readable = [fr"{item}" for item in nml2_human_readable]

    longest_line1 = len(max(nml1_human_readable, key=len)) + 3

    # PG: BAD HACK:
    longest_line1 = longest_line_global

    f1.seek(0)
    f2.seek(0)

    f3 = tempfile.NamedTemporaryFile(mode="w+")
    for line in f1.readlines():
        f3.write(ansi_ljust(line.rstrip("\n"), longest_line1) + "\n")
        # f3.write(line.rstrip("\n").ljust(longest_line1)+"\n")

    f3.seek(0)
    f4 = tempfile.NamedTemporaryFile(mode="w+")
    for old_line, new_line in zip_longest(f3.readlines(), f2.readlines()):
        if old_line and new_line:
            f4.write(old_line.rstrip("\n") + " | " + new_line)
        elif old_line:
            f4.write(old_line.rstrip("\n") + " |\n")
        elif new_line:
            f4.write(" ".ljust(longest_line1) + "| " + new_line)

    f4.seek(0)
    for line in f4.readlines():
        print(line.rstrip("\n"))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
