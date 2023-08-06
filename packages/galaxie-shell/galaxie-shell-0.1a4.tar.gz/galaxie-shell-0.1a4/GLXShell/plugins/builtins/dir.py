import os
import cmd2
import argparse

from GLXShell.plugins.builtins import __version__
from GLXShell.plugins.builtins import __appname__
from GLXShell.plugins.builtins import __licence__

dir_parser = argparse.ArgumentParser()
dir_parser.add_argument(
    "-l",
    "--long",
    action="store_true",
    help="display in long format with one item per line",
)
dir_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)


class GLXDir(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    @staticmethod
    def dir_print_version():
        cmd2.Cmd().poutput(
            "dir ({0}) v{1}\n{2}".format(__appname__, __version__, __licence__)
        )

    @cmd2.with_argparser(dir_parser, with_unknown_args=True)
    @cmd2.with_category("Builtins")
    def do_dir(self, args, unknown):
        """List contents of current directory."""
        if args.version:
            self.dir_print_version()
            return

        # No arguments for this commands
        if unknown:
            cmd2.Cmd().perror("dir does not take any positional arguments:")
            dir_parser.print_help()
            cmd2.Cmd().last_result = "Bad arguments"
            return

        # Get the contents as a list
        contents = os.listdir(os.getcwd())
        for f in contents:
            cmd2.Cmd().poutput(f"{f}")

        cmd2.Cmd().last_result = contents
