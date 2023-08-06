import os
import cmd2
import argparse

from GLXShell.plugins.builtins import __version__
from GLXShell.plugins.builtins import __appname__
from GLXShell.plugins.builtins import __licence__

which_parser = cmd2.Cmd2ArgumentParser(
    description="which  returns  the pathnames of the files (or links) which would be executed in the current "
    "environment, had its arguments been given as commands in a strictly POSIX-conformant shell.  It does "
    "this by searching the PATH for executable files matching the names  of  the arguments. It does not "
    "canonicalize path names. "
)
which_parser.add_argument(
    "-a",
    "--all",
    action="store_true",
    help="print all matching pathnames of each argument",
)

which_parser.add_argument(
    "--version",
    action="store_true",
    help="output version information and exit",
)

which_parser.add_argument(
    "filename",
    nargs="?",
    const=1,
)


class GLXWhich(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    @staticmethod
    def which_print_version():
        cmd2.Cmd().poutput(
            "which ({name}) v{version}\n{licence}".format(
                name=__appname__,
                version=__version__,
                licence=__licence__,
            )
        )

    @staticmethod
    def which(all_info=False, filename=None):
        for exec_path in os.get_exec_path():
            if os.path.isfile(os.path.join(exec_path, filename)):
                if os.access(os.path.join(exec_path, filename), os.X_OK):
                    cmd2.Cmd().poutput(os.path.join(exec_path, filename))
                    if not all_info:
                        return

    @cmd2.with_argparser(which_parser)
    @cmd2.with_category("Builtins")
    def do_which(self, args):
        if args.version:  # pragma: no cover
            self.which_print_version()
            return

        if args.filename is None:  # pragma: no cover
            which_parser.print_usage()
            return

        self.which(all_info=args.all, filename=args.filename)  # pragma: no cover
