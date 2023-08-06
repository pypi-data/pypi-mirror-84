import os
import cmd2
import argparse
import sys

# https://www.maizure.org/projects/decoded-gnu-coreutils/
# https://www.maizure.org/projects/decoded-gnu-coreutils/cat.html

from GLXShell.plugins.builtins import __version__
from GLXShell.plugins.builtins import __appname__
from GLXShell.plugins.builtins import __licence__

cat_parser = argparse.ArgumentParser()
cat_parser.add_argument(
    "file",
    nargs="*",
    type=argparse.FileType("r"),
    default=sys.stdin,
    help="with no FILE, or when FILE is -, read standard input.",
)
#   -A, --show-all           equivalent to -vET
cat_parser.add_argument(
    "-A",
    "--show-all",
    action="store_true",
    help="equivalent to -vET",
)
#   -b, --number-nonblank    number nonempty output lines, overrides -n
cat_parser.add_argument(
    "-b",
    "--number-nonblank",
    action="store_true",
    help="number nonempty output lines, overrides -n",
)
#   -e                       equivalent to -vE
cat_parser.add_argument(
    "-e",
    action="store_true",
    help="equivalent to -vE",
)
#   -E, --show-ends          display $ at end of each line
cat_parser.add_argument(
    "-E",
    "--show-ends",
    action="store_true",
    help="display $ at end of each line",
)
#   -n, --number             number all output lines
cat_parser.add_argument(
    "-n",
    "--number",
    action="store_true",
    help="number all output lines",
)
#   -s, --squeeze-blank      suppress repeated empty output lines
cat_parser.add_argument(
    "-s",
    "--squeeze-blank",
    action="store_true",
    help="suppress repeated empty output lines",
)
#   -t                       equivalent to -vT
cat_parser.add_argument(
    "-t",
    action="store_true",
    help="equivalent to -vT",
)
#   -T, --show-tabs          display TAB characters as ^I
cat_parser.add_argument(
    "-T",
    "--show-tabs",
    action="store_true",
    help="display TAB characters as ^I",
)
#   -u                       (ignored)
cat_parser.add_argument(
    "-u",
    action="store_true",
    help="(ignored)",
)
#   -v, --show-nonprinting   use ^ and M- notation, except for LFD and TAB
cat_parser.add_argument(
    "-v",
    "--show-nonprinting",
    action="store_true",
    help="use ^ and M- notation, except for LFD and TAB",
)
#      --help               display this help and exit
#      --version            output version information and exit
cat_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)


class GLXCat(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    @staticmethod
    def cat_print_version():
        cmd2.Cmd().poutput(
            "cat (0) v{1}\n{2}".format(__appname__, __version__, __licence__)
        )

    @cmd2.with_argparser(cat_parser)
    @cmd2.with_category("Builtins")
    def do_cat(self, args):
        """Concatenate FILE(s) to standard output"""
        if args.version:
            self.cat_print_version()
            return

        if args.number_nonblank:
            args.number = False

        file_data = []
        for file in args.file:
            file_data.append(file.read().split("\n"))

        think_to_display = []
        line_number = 1
        blank_line_allowed = True

        for file in file_data:
            if not blank_line_allowed:
                blank_line_allowed = True

            for line in file:
                if args.show_tabs:
                    line = line.replace("\t", "^I")
                if args.number:
                    if len(line) > 0:
                        think_to_display.append(
                            "{0:>6d}  {1}".format(line_number, line)
                        )
                        line_number += 1
                        if not blank_line_allowed:
                            blank_line_allowed = True
                    else:
                        if blank_line_allowed:
                            think_to_display.append(
                                "{0:>6d}  {1}".format(line_number, "")
                            )
                            line_number += 1
                            if args.squeeze_blank and blank_line_allowed:
                                blank_line_allowed = False

                elif args.number_nonblank:
                    if len(line) > 0:
                        think_to_display.append(
                            "{0:>6d}  {1}".format(line_number, line)
                        )
                        line_number += 1
                        if not blank_line_allowed:
                            blank_line_allowed = True
                    else:
                        if blank_line_allowed:
                            think_to_display.append("")
                            if args.squeeze_blank and blank_line_allowed:
                                blank_line_allowed = False
                else:
                    if len(line) > 0:
                        think_to_display.append(line)
                        if not blank_line_allowed:
                            blank_line_allowed = True
                    else:
                        if blank_line_allowed:
                            think_to_display.append(line)
                            if args.squeeze_blank and blank_line_allowed:
                                blank_line_allowed = False

        if args.show_ends:
            cmd2.Cmd().last_result = "$\n".join(think_to_display)
        else:
            cmd2.Cmd().last_result = "\n".join(think_to_display)
        cmd2.Cmd().poutput(msg=cmd2.Cmd().last_result, end="")

    @staticmethod
    def complete_cat(text, line, begidx, endidx):
        return cmd2.Cmd().path_complete(
            text, line, begidx, endidx, path_filter=os.path.exists
        )

