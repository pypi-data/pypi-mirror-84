import cmd2

from GLXShell.libs.properties.shortcuts import GLXShPropertyShortcuts
from GLXShell.libs.properties.history import GLXShPropertyHistory
from GLXShell.libs.properties.config import GLXShPropertyConfig
from GLXShell.libs.properties.shell import GLXShPropertyShell
from GLXShell.libs.utils.get_terminal_size import get_terminal_size
from GLXShell.libs.plugins import GLXShPluginsManager
from GLXShell.libs.intro import GLXShIntro
from GLXShell.libs.prompt import GLXShPrompt
from GLXShell.libs.settable import GLXShSettable


# Key binding
# http://readline.kablamo.org/emacs.html


class GLXShell(
    GLXShPropertyShortcuts,
    GLXShPropertyHistory,
    GLXShPropertyConfig,
    GLXShPropertyShell,
    GLXShIntro,
    GLXShPrompt,
    GLXShPluginsManager,
    cmd2.Cmd,
    GLXShSettable,
):
    def __init__(self):
        GLXShPropertyShortcuts.__init__(self)
        GLXShPropertyHistory.__init__(self)
        GLXShPropertyConfig.__init__(self)
        GLXShPropertyShell.__init__(self)
        GLXShIntro.__init__(self)
        GLXShPrompt.__init__(self)

        # Init and config the cmd2 object
        cmd2.Cmd.__init__(
            self,
            persistent_history_file=self.persistent_history_file,
            persistent_history_length=self.persistent_history_length,
            shortcuts=self.shortcuts,
            auto_load_commands=False,
            allow_cli_args=True,
        )
        self.allow_redirection = True
        self.default_to_shell = True

        # PostProcessing
        GLXShPluginsManager(self).load_plugins()
        GLXShSettable(self).load_settable()

    @property
    def intro(self):
        """Return intro to displays"""
        self.columns, self.rows = get_terminal_size()
        return self.intro_to_display

    @property
    def prompt(self):
        """Return prompt to displays"""
        return self.prompt_to_display
