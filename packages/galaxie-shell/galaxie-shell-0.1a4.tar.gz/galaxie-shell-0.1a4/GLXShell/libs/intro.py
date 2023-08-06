# !/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Shell Team, all rights reserved

import os
import sys
import platform

from GLXShell import __version__
from GLXShell import __appname__
from GLXShell.libs.utils.info_memory import get_memory_total
from GLXShell.libs.utils.info_memory import get_memory_available
from GLXShell.libs.utils.info_memory import get_size
from GLXShell.libs.config import GLXShConfig


class GLXShIntro(object):
    def __init__(self, *args, **kwargs):
        self.config = kwargs.get("config", GLXShConfig())

        have_change = False
        if "intro" not in self.config.data:
            self.config.data["intro"] = {}
            have_change = True

        if "show" not in self.config.data["intro"]:
            self.config.data["intro"]["show"] = {}
            have_change = True

        if have_change:
            self.config.write()

        self.rows = 24
        self.columns = 80

        self.__intro_show_title = None
        self.__intro_show_spacing = None
        self.__intro_show_license = None
        self.__intro_show_loader = None
        self.__intro_show_exec = None
        self.__intro_show_memory_total = None
        self.__intro_show_memory_free = None
        self.__intro_show_holotape = None
        self.__intro_show_rom = None

        try:
            self.intro_show_exec = self.config.data["intro"]["show"]["exec"]
        except KeyError:
            self.intro_show_exec = None
        try:
            self.intro_show_holotape = self.config.data["intro"]["show"]["holotape"]
        except KeyError:
            self.intro_show_holotape = None
        try:
            self.intro_show_license = self.config.data["intro"]["show"]["license"]
        except KeyError:
            self.intro_show_license = None
        try:
            self.intro_show_loader = self.config.data["intro"]["show"]["loader"]
        except KeyError:
            self.intro_show_loader = None
        try:
            self.intro_show_memory_free = self.config.data["intro"]["show"][
                "memory_free"
            ]
        except KeyError:
            self.intro_show_memory_free = None
        try:
            self.intro_show_memory_total = self.config.data["intro"]["show"][
                "memory_total"
            ]
        except KeyError:
            self.intro_show_memory_total = None
        try:
            self.intro_show_rom = self.config.data["intro"]["show"]["rom"]
        except KeyError:
            self.intro_show_rom = None
        try:
            self.intro_show_spacing = self.config.data["intro"]["show"]["spacing"]
        except KeyError:
            self.intro_show_spacing = None
        try:
            self.intro_show_title = self.config.data["intro"]["show"]["title"]
        except KeyError:
            self.intro_show_title = None

    @property
    def title(self):
        return "{app_name} V{version}".format(
            app_name=__appname__.upper(), version=__version__.upper()
        )

    @property
    def title_line(self):
        return "{text_inner} {text} {text_outer}".format(
            text=self.title,
            text_inner="*" * int((int(self.columns) / 2) - (len(self.title) / 2) - 1),
            text_outer="*" * int((int(self.columns) / 2) - (len(self.title) / 2) - 1),
        )

    @property
    def intro_show_exec(self):
        return self.__intro_show_exec

    @intro_show_exec.setter
    def intro_show_exec(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'exec' property value must be a bool type or None")
        if self.intro_show_exec != value:
            self.__intro_show_exec = value
        if (
            "exec" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["exec"] != value
        ):
            self.config.data["intro"]["show"]["exec"] = value
            self.config.write()

    @property
    def intro_show_holotape(self):
        return self.__intro_show_holotape

    @intro_show_holotape.setter
    def intro_show_holotape(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'holotape' property value must be a bool type or None")
        if self.intro_show_holotape != value:
            self.__intro_show_holotape = value
        if (
            "holotape" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["holotape"] != value
        ):
            self.config.data["intro"]["show"]["holotape"] = value
            self.config.write()

    @property
    def intro_show_license(self):
        return self.__intro_show_license

    @intro_show_license.setter
    def intro_show_license(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'license' property value must be a bool type or None")
        if self.intro_show_license != value:
            self.__intro_show_license = value
        if (
            "license" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["license"] != value
        ):
            self.config.data["intro"]["show"]["license"] = value
            self.config.write()

    @property
    def intro_show_loader(self):
        return self.__intro_show_loader

    @intro_show_loader.setter
    def intro_show_loader(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'loader' property value must be a bool type or None")
        if self.intro_show_loader != value:
            self.__intro_show_loader = value
        if (
            "loader" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["loader"] != value
        ):
            self.config.data["intro"]["show"]["loader"] = value
            self.config.write()

    @property
    def intro_show_memory_free(self):
        return self.__intro_show_memory_free

    @intro_show_memory_free.setter
    def intro_show_memory_free(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'memory_free' property value must be a bool type or None")
        if self.intro_show_memory_free != value:
            self.__intro_show_memory_free = value
        if (
            "memory_free" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["memory_free"] != value
        ):
            self.config.data["intro"]["show"]["memory_free"] = value
            self.config.write()

    @property
    def intro_show_memory_total(self):
        return self.__intro_show_memory_total

    @intro_show_memory_total.setter
    def intro_show_memory_total(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'memory_total' property value must be a bool type or None")
        if self.intro_show_memory_total != value:
            self.__intro_show_memory_total = value
        if (
            "memory_total" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["memory_total"] != value
        ):
            self.config.data["intro"]["show"]["memory_total"] = value
            self.config.write()

    @property
    def intro_show_rom(self):
        return self.__intro_show_rom

    @intro_show_rom.setter
    def intro_show_rom(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'rom' property value must be a bool type or None")
        if self.intro_show_rom != value:
            self.__intro_show_rom = value
        if (
            "rom" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["rom"] != value
        ):
            self.config.data["intro"]["show"]["rom"] = value
            self.config.write()

    @property
    def intro_show_spacing(self):
        return self.__intro_show_spacing

    @intro_show_spacing.setter
    def intro_show_spacing(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError(
                "'intro_show_spacing' property value must be a bool type or None"
            )
        if self.intro_show_spacing != value:
            self.__intro_show_spacing = value
        if (
            "spacing" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["spacing"] != value
        ):
            self.config.data["intro"]["show"]["spacing"] = value
            self.config.write()

    @property
    def intro_show_title(self):
        return self.__intro_show_title

    @intro_show_title.setter
    def intro_show_title(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError(
                "'intro_show_title' property value must be a bool type or None"
            )
        if self.intro_show_title != value:
            self.__intro_show_title = value
        if (
            "title" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["title"] != value
        ):
            self.config.data["intro"]["show"]["title"] = value
            self.config.write()

    def onchange_intro_show_exec(self, param_name, old_value, new_value):
        pass

    def onchange_intro_show_holotape(self, param_name, old_value, new_value):
        pass

    def onchange_intro_show_license(self, param_name, old_value, new_value):
        pass

    def onchange_intro_show_loader(self, param_name, old_value, new_value):
        pass

    def onchange_intro_show_memory_free(self, param_name, old_value, new_value):
        pass

    def onchange_intro_show_memory_total(self, param_name, old_value, new_value):
        pass

    def onchange_intro_show_rom(self, param_name, old_value, new_value):
        pass

    def onchange_intro_show_spacing(self, param_name, old_value, new_value):
        pass

    def onchange_intro_show_title(self, param_name, old_value, new_value):
        pass

    @property
    def intro_to_display(self):
        if os.environ.get("VIRTUAL_ENV") or os.environ.get("CONDA_DEFAULT_ENV"):
            exec_venv = "VENV"
        else:
            exec_venv = "ENV"
        to_return = []
        if self.intro_show_title:
            to_return.append(self.title_line)
            if self.intro_show_spacing:
                to_return.append("")
                to_return.append("")
        if self.intro_show_license:
            to_return.append("GNU GENERAL PUBLIC LICENSE GPL-3.0")
        if self.intro_show_loader:
            to_return.append("LOADER {0}".format(platform.version().upper()))
        if self.intro_show_exec:
            to_return.append(
                "EXEC {exec_venv} PYTHON {python_version_major}.{python_version_minor}.{python_version_micro}".format(
                    exec_venv=exec_venv,
                    python_version_major=sys.version_info.major,
                    python_version_minor=sys.version_info.minor,
                    python_version_micro=sys.version_info.micro,
                )
            )
        if self.intro_show_memory_total:
            to_return.append(
                "{mem_total} RAM SYSTEM".format(mem_total=get_size(get_memory_total()))
            )
        if self.intro_show_memory_free:
            to_return.append(
                "{mem_available} FREE".format(
                    mem_available=get_size(get_memory_available())
                )
            )
        if self.intro_show_holotape:
            to_return.append("NO HOLOTAPE FOUND")
        if self.intro_show_rom:
            to_return.append("LOAD ROM(1): DEITRIX 303")
        if self.intro_show_spacing:
            to_return.append("")

        return "\n".join(to_return)
