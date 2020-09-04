"""Console script for namelist_diff."""
import argparse
import sys
import tempfile
from itertools import zip_longest

import dictdiffer
import f90nml

from .namelist_diff import (
    NamelistDiff
        )

from .config import (load_config, write_default_config)

def main():
    """Console script for namelist_diff."""
    parser = argparse.ArgumentParser()
    parser.add_argument("nml1")
    parser.add_argument("nml2")
    parser.add_argument("--keep_mvstreamctl", action="store_true")
    parser.add_argument("--keep_set_stream", action="store_true")
    parser.add_argument("--keep_set_stream_element", action="store_true")
    parser.add_argument("--raw_paths", action="store_true")
    parser.add_argument("--write-default-config", action="store_true")
    args = parser.parse_args()

    if args.write_default_config:
        write_default_config()
        return 0  # exit code for the CLI...

    print("Comparison for namelists")
    print("------------------------")
    print(f"1st namelist \t {args.nml1}")
    print(f"2nd namelist \t {args.nml2}")

    nmldiff = NamelistDiff(args.nml1, args.nml2)
    nmldiff.diff()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
