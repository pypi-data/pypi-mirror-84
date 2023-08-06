#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Shell Team, all rights reserved

import os
import json

from GLXShell.libs.utils.xdg_base_directory import XDGBaseDirectory
from GLXShell.libs.utils.singleton import Singleton


class GLXShConfig(XDGBaseDirectory, metaclass=Singleton):
    def __init__(self):
        XDGBaseDirectory.__init__(self)

        self.__file = None
        self.__data = None

        self.file = None
        self.data = None

        self.touch()
        self.load()

    @property
    def file(self):
        """
        Property it store configuration file path

        Note: Default is XDGBaseDirectory/glxsh

        :return: the config file path
        :rtype: str
        """
        return self.__file

    @file.setter
    def file(self, value=None):
        """
        Set the ``config_file_path`` property value

        Note: if ``config_file_path`` property value is set to ``None``
        it will restore default value: XDGBaseDirectory/glxsh

        :param value: the config file path
        :type value: str or None
        """
        if value is None:
            value = os.path.join(self.config_path, "config.json")
        if type(value) != str:
            raise TypeError("'config_file' property value must be a str type or None")
        if value != self.file:
            self.__file = value
            # self.load()

    @property
    def data(self):
        """
        A dictionary it contain all the setting

        :return: the setting
        :rtype: dict
        """
        return self.__data

    @data.setter
    def data(self, value=None):
        """
        Set the ``data`` property

        Note: If ``data`` property value is ``None`` is restore a empty dictionary setting

        :param value: the setting
        :return: dict or None
        :raise TypeError: When ``data`` property value is not dict type or None
        """
        if value is None:
            value = {}
        if type(value) != dict:
            raise TypeError("'data' property value must be a dict type or None")
        if self.data != value:
            self.__data = value

    def touch(self):
        """Create directory where store the configuration file and if the config file do not exist
        create one with a empty dictionary
        """
        if not os.path.exists(os.path.dirname(self.file)):
            os.makedirs(os.path.dirname(self.file))
        if not os.path.exists(self.file):
            with open(self.file, "w") as outfile:
                json.dump({}, outfile)

    def load(self):
        """Load the configuration file and update ``data`` property"""
        with open(self.file, "r") as json_data_file:
            self.data.update(json.load(json_data_file))

    def write(self):
        """Write ``data`` property content inside the configuration file"""
        with open(self.file, "w") as outfile:
            json.dump(self.data, outfile, sort_keys=True, indent=4)
