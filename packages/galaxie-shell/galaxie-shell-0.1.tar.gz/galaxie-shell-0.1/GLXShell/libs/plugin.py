import cmd2

from GLXShell.libs.properties.shell import GLXShPropertyShell
from GLXShell.libs.properties.commands import GLXShellPropertyCommands


class GLXShellPlugin(GLXShPropertyShell, GLXShellPropertyCommands):
    def __init__(self):
        GLXShPropertyShell.__init__(self)
        GLXShellPropertyCommands.__init__(self)

    def load(self):
        if self.shell.debug:
            cmd2.Cmd().pwarning("PLUGINS LOAD ...")
        for cmd in self.commands:
            try:
                self.shell.register_command_set(cmd["object"])
                if self.shell.debug:
                    cmd2.Cmd().pwarning("{0}".format(cmd["name"]))
            except cmd2.CommandSetRegistrationError:
                cmd2.Cmd().perror("{0} already loaded".format(cmd["name"]))

    def unload(self):
        if self.shell.debug:
            cmd2.Cmd().pwarning("PLUGINS UNLOAD ...")
        for cmd in self.commands:
            self.shell.unregister_command_set(cmd["object"])
            if self.shell.debug:
                cmd2.Cmd().pwarning("{0}".format(cmd["name"]))

    def reload(self):
        self.unload()
        self.load()
