"""Main module."""
import logging
import pdb
import tempfile
from functools import wraps

from ansiwrap import ansilen
import colorama
import f90nml


longest_line_global = 0


class NamelistDiff:

    _cleanup_funcs = []

    def __init__(self, nml1, nml2, config):
        if not isinstance(nml1, f90nml.Namelist):
            nml1 = f90nml.read(nml1)
        if not isinstnace(nml2, f90nml.Namelist):
            nml2 = f90nml.read(nml2)

        self._cleanup_namelist(nml1)
        self._cleanup_namelist(nml2)

        self.nml1 = nml1
        self.nml2 = nml2

    @staticmethod
    def _cleanup_namelist(nml):
        for cleanup_func in _cleanup_funcs:
            nml = cleanup_func(nml)

    @staticmethod
    def _cleanup_func():

        @wraps(meth)
        def wrapped_meth(meth, *args, **kwargs):
            _cleanup_funcs.append(meth.__name__)
            return meth(*args, **kwargs)
        return wrapped_meth

    def diff(self):
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


def ansi_ljust(s, width):
    needed = width - ansilen(s)
    if needed > 0:
        return s + " " * needed
    else:
        return s


def namelist_to_iter(nml):
    try:
        f = tempfile.TemporaryFile(mode="w+")
        nml.write(f)
        f.seek(0)
        nml_human_readable = f.readlines()
        f.close()
        return nml_human_readable
    except AttributeError:
        import pdb

        pdb.set_trace()
    except Exception:
        raise


def determine_print_prefix(diff_type):
    if diff_type == "change":
        nml_print = "~"
    elif diff_type == "add":
        nml_print = "+"
    elif diff_type == "remove":
        nml_print = "-"
    return nml_print


def color_string(s, color):
    return getattr(colorama.Fore, color) + s + colorama.Fore.RESET


def color_yellow(s):
    return color_string(s, "YELLOW")


def color_red(s):
    return color_string(s, "RED")


def color_green(s):
    return color_string(s, "GREEN")


def determine_print_color(diff_type):
    if diff_type == "change":
        # nml_print = crayons.yellow
        nml_print = color_yellow
    elif diff_type == "add":
        nml_print = color_green
    elif diff_type == "remove":
        nml_print = color_red
    return nml_print


def check_longest_line(s):
    global longest_line_global
    if len(s) > longest_line_global:
        longest_line_global = len(s)


def format_entry(current_chapter, current_entry, all_diffs):
    current_key, current_value = current_entry
    for current_diff in all_diffs:
        diff_type, rest = current_diff[0], current_diff[1:]
        nml_print = determine_print_color(diff_type)
        if isinstance(rest[0], str):
            diff_chapter = rest[0].split(".")[0]
        elif isinstance(rest[0], list):
            diff_chapter = rest[0][0]
        else:
            print(rest[0])
            raise TypeError("Don't know how to handle that yet!")

        if not current_chapter == diff_chapter:
            continue
        if diff_type == "change":
            if isinstance(rest[0], str):
                diff_key = rest[0].split(".")[1:]
                if len(diff_key) == 1:
                    diff_key = diff_key[0]
            elif isinstance(rest[0], list):
                diff_key = rest[0][1]
            else:

                pdb.set_trace()
            # Check current entry vs diff entry:
            if current_key != diff_key:
                continue  # Reset loop, not the same keys
            old_value, new_value = rest[1]
            # Remove the diff, it has been solved:
            all_diffs.remove(current_diff)
            s = nml_print("~    {}{}{}".format(diff_key, " = ", old_value))
            check_longest_line(s)
            return s
        if diff_type == "add":
            try:
                new_key, new_value = rest[1].pop()
            except IndexError:
                import pdb

                pdb.set_trace()
            all_diffs.remove(current_diff)
            s = nml_print("+    {}{}{}".format(new_key, " = ", new_value))
            check_longest_line(s)
            return s
        if diff_type == "remove":
            all_diffs.remove(current_diff)
            s = nml_print("-    {}{}{}".format(rest[1][0][0], " = ", rest[1][0][1]))
            check_longest_line(s)
            return s
        raise ValueError("Unknown Diff Type...")
    s = "    {}{}{}".format(current_key, " = ", current_value)
    check_longest_line(s)
    return s


def format_remaining_diff(current_diff, all_diffs):
    return_list = []
    diff_type, rest = current_diff[0], current_diff[1:]
    nml_prefix = determine_print_prefix(diff_type)
    dummy_chapter, chapter = rest
    try:
        assert dummy_chapter == ""
    except AssertionError:
        import pdb

        pdb.set_trace()
    while chapter:
        new_chapter_name, new_chapter_nml = chapter.pop()
        assert isinstance(new_chapter_nml, f90nml.Namelist)
        # return_list.append(nml_print(f"&{chapter}"))
        for line in namelist_to_iter(
            f90nml.Namelist({new_chapter_name: new_chapter_nml})
        ):
            s = nml_prefix + line
            check_longest_line(s)
            return_list.append(nml_prefix + line)
    all_diffs.remove(current_diff)
    return_str = [item + "" for item in return_list]
    return "".join(return_str)


def format_nml(nml, fhdl, diff):
    all_diffs = list(diff)
    while all_diffs:
        for chapter in nml:
            fhdl.write(f"&{chapter}\n")
            raw_entries = list(nml[chapter].items())
            while raw_entries:
                current_entry = raw_entries.pop()
                formatted_entry = format_entry(chapter, current_entry, all_diffs)
                fhdl.write(formatted_entry + "\n")
            fhdl.write("/\n")
        logging.debug("Diffs remaining after looping over all chapters:")
        logging.debug(all_diffs)
        for diff in all_diffs:
            formatted_diff = format_remaining_diff(diff, all_diffs)
            fhdl.write(formatted_diff + "\n")
        logging.debug("Diffs remaining after exotic diffs:")
        logging.debug(all_diffs)
        break
