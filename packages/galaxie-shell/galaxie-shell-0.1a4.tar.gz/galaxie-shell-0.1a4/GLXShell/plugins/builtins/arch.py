import os
import argparse
import cmd2

from GLXShell.plugins.builtins import __version__
from GLXShell.plugins.builtins import __appname__
from GLXShell.plugins.builtins import __licence__

arch_parser = argparse.ArgumentParser(description="Print machine architecture.")
#      --help               display this help and exit
#      --version            output version information and exit
arch_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)


class GLXArch(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    @property
    def result(self):
        return f"{os.uname().machine}"

    @staticmethod
    def arch_print_version():
        cmd2.Cmd().poutput(
            "arch ({name}) v{version}\n{licence}".format(
                name=__appname__,
                version=__version__,
                licence=__licence__,
            )
        )

    def arch(self):
        cmd2.Cmd().last_result = self.result
        cmd2.Cmd().poutput(self.result)

    @cmd2.with_argparser(arch_parser)
    @cmd2.with_category("Builtins")
    def do_arch(self, args):
        if args.version:  # pragma: no cover
            self.arch_print_version()
            return

        self.arch()  # pragma: no cover
