#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import os
import getpass
import socket

from GLXShell.libs.config import GLXShConfig


class GLXShPrompt(object):
    def __init__(self, *args, **kwargs):
        self.config = kwargs.get("config", GLXShConfig())

        have_change = False

        if "prompt" not in self.config.data:
            self.config.data["prompt"] = {}
            have_change = True

        if "show" not in self.config.data["prompt"]:
            self.config.data["prompt"]["show"] = {}
            have_change = True

        if have_change:
            self.config.write()

        self.__prompt_show_info = None
        self.__prompt_show_cursor = None

        try:
            self.prompt_show_cursor = self.config.data["prompt"]["show"]["cursor"]
        except KeyError:
            self.prompt_show_cursor = None
        try:
            self.prompt_show_info = self.config.data["prompt"]["show"]["info"]
        except KeyError:
            self.prompt_show_info = None

    @property
    def prompt_show_info(self):
        return self.__prompt_show_info

    @prompt_show_info.setter
    def prompt_show_info(self, value=None):
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError(
                "'prompt_show_info' property value must be a bool type or None"
            )
        if self.prompt_show_info != value:
            self.__prompt_show_info = value
        if (
            "info" not in self.config.data["prompt"]["show"]
            or self.config.data["prompt"]["show"]["info"] != value
        ):
            self.config.data["prompt"]["show"]["info"] = value
            self.config.write()

    @property
    def prompt_show_cursor(self):
        return self.__prompt_show_cursor

    @prompt_show_cursor.setter
    def prompt_show_cursor(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError(
                "'prompt_show_cursor' property value must be a bool type or None"
            )
        if self.prompt_show_cursor != value:
            self.__prompt_show_cursor = value
        if (
            "cursor" not in self.config.data["prompt"]["show"]
            or self.config.data["prompt"]["show"]["cursor"] != value
        ):
            self.config.data["prompt"]["show"]["cursor"] = value
            self.config.write()

    def onchange_prompt_show_cursor(self, param_name, old_value, new_value):
        pass

    def onchange_prompt_show_info(self, param_name, old_value, new_value):
        pass

    @property
    def prompt_env_is_virtual(self):
        if os.environ.get("VIRTUAL_ENV") or os.environ.get("CONDA_DEFAULT_ENV"):
            return True
        else:
            return False

    @property
    def prompt_env_text(self):
        if os.environ.get("VIRTUAL_ENV") or os.environ.get("CONDA_DEFAULT_ENV"):
            env_path = os.environ.get("VIRTUAL_ENV", "")
            if len(env_path) == 0:
                env_path = os.environ.get("CONDA_DEFAULT_ENV", "")

            return "({env_name}) ".format(env_name=os.path.basename(env_path))
        else:
            return ""

    @property
    def prompt_username_text(self):
        return getpass.getuser()

    @property
    def prompt_hostname_text(self):
        return socket.gethostname()

    @property
    def prompt_path_text(self):
        return os.getcwd().replace(os.path.realpath(os.path.expanduser("~")), "~")

    @property
    def prompt_symbol_text(self):
        if os.getuid() == 0:  # pragma: no cover
            return "#"
        else:
            return "$"

    @property
    def prompt_cursor_text(self):
        return ">"

    @property
    def prompt_to_display(self):
        """Set prompt so it displays the current working directory."""
        prompt = []
        if self.prompt_show_info:
            prompt.append(
                "{venv}{username}@{hostname}:{path} {symbol} ".format(
                    venv=self.prompt_env_text,
                    username=self.prompt_username_text,
                    hostname=self.prompt_hostname_text,
                    path=self.prompt_path_text,
                    symbol=self.prompt_symbol_text,
                )
            )
        if self.prompt_show_cursor:
            prompt.append("{cursor} ".format(cursor=self.prompt_cursor_text))

        return "\n".join(prompt)
