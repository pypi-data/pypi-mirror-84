#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Shell Team, all rights reserved

import argparse
import cmd2

from GLXShell.libs.properties.plugins import GLXShellPropertyPlugins
from GLXShell.plugins.builtins import GLXShPluginBuiltins
from GLXShell.libs.config import GLXShConfig

managed = [
    {"name": "builtins", "object": GLXShPluginBuiltins()},
]


def choices():
    to_return = []
    for plugin in managed:
        if plugin and "name" in plugin:
            to_return.append(plugin["name"])
    return to_return


class GLXShPluginsManager(GLXShellPropertyPlugins):
    def __init__(self, *args, **kwargs):
        GLXShellPropertyPlugins.__init__(self)
        self.plugins = managed

        self.config = kwargs.get("config", GLXShConfig())
        try:
            shell = args[0]
        except IndexError:
            shell = None
        self.shell = kwargs.get("shell", shell)

        have_change = False

        if "plugins" not in self.config.data:
            self.config.data["plugins"] = {}
            have_change = True

        for plugin in self.plugins:
            if plugin["name"] not in self.config.data["plugins"]:
                self.config.data["plugins"][plugin["name"]] = {}
                have_change = True
            if "enabled" not in self.config.data["plugins"][plugin["name"]]:
                self.config.data["plugins"][plugin["name"]]["enabled"] = True
                have_change = True

        if have_change:
            self.config.write()

    def load_plugins(self):
        for plugin in self.plugins:
            if self.config.data["plugins"][plugin["name"]]["enabled"]:
                plugin["object"].shell = self.shell
                plugin["object"].load()

    enable_parser = cmd2.Cmd2ArgumentParser()
    enable_parser.add_argument("name", choices=choices())

    @cmd2.as_subcommand_to("plugins", "enable", enable_parser)
    @cmd2.with_category("Plugins commands")
    def enable(self, ns: argparse.Namespace):
        """Enable at startup a plugin by it name and load it"""
        for plugin in self.plugins:
            if ns.name == plugin["name"]:
                plugin["object"].shell = self.shell
                plugin["object"].load()
                if not self.config.data["plugins"][plugin["name"]]["enabled"]:
                    self.config.data["plugins"][plugin["name"]]["enabled"] = True
                    self.config.write()

    disable_parser = cmd2.Cmd2ArgumentParser()
    disable_parser.add_argument("name", choices=choices())

    @cmd2.as_subcommand_to("plugins", "disable", disable_parser)
    @cmd2.with_category("Plugins commands")
    def disable(self, ns: argparse.Namespace):
        """Disable at startup a plugin by it name and unload it"""
        for plugin in self.plugins:
            if ns.name == plugin["name"]:
                plugin["object"].shell = self.shell
                plugin["object"].unload()
                if self.config.data["plugins"][plugin["name"]]["enabled"]:
                    self.config.data["plugins"][plugin["name"]]["enabled"] = False
                    self.config.write()

    load_parser = cmd2.Cmd2ArgumentParser()
    load_parser.add_argument("name", choices=choices())

    @cmd2.as_subcommand_to("plugins", "load", load_parser)
    @cmd2.with_category("Plugins commands")
    def load(self, ns: argparse.Namespace):
        """Load a plugin by it name"""
        for plugin in self.plugins:
            if ns.name == plugin["name"]:
                plugin["object"].shell = self.shell
                plugin["object"].load()

    unload_parser = cmd2.Cmd2ArgumentParser()
    unload_parser.add_argument("name", choices=choices())

    @cmd2.as_subcommand_to("plugins", "unload", unload_parser)
    @cmd2.with_category("Plugins commands")
    def unload(self, ns: argparse.Namespace):
        """Unload a plugin by it name"""
        for plugin in self.plugins:
            if ns.name == plugin["name"]:
                plugin["object"].shell = self.shell
                plugin["object"].unload()

    reload_parser = cmd2.Cmd2ArgumentParser()
    reload_parser.add_argument("name", choices=choices())

    @cmd2.as_subcommand_to("plugins", "reload", reload_parser)
    @cmd2.with_category("Plugins commands")
    def reload(self, ns: argparse.Namespace):
        """Reload a plugin by it name"""
        for plugin in self.plugins:
            if ns.name == plugin["name"]:
                plugin["object"].shell = self.shell
                plugin["object"].reload()

    plugins_parser = cmd2.Cmd2ArgumentParser(description="Plugins management")
    plugins_subparsers = plugins_parser.add_subparsers(
        title="commands", help="a command it can be choose"
    )

    @cmd2.with_argparser(plugins_parser)
    @cmd2.with_category("Plugins")
    def do_plugins(self, ns: argparse.Namespace):
        handler = ns.cmd2_handler.get()  # pragma: no cover
        if handler is not None:  # pragma: no cover
            # Call whatever subcommand function was selected
            handler(ns)
        else:  # pragma: no cover
            # No subcommand was provided, so call help
            cmd2.Cmd().perror("This command does nothing without sub-commands")
            self.shell.do_help("plugins")
