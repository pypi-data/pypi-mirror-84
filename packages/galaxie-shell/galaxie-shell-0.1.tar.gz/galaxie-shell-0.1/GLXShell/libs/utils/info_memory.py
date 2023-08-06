#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Shell Team, all rights reserved

import os


def get_memory_total():
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    except ValueError:  # pragma: no cover
        return 0


def get_memory_available():
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_AVPHYS_PAGES")
    except ValueError:  # pragma: no cover
        return 0


def get_size(size, suffix="B"):
    """
    Scale bytes to its proper format

    e.g: 1253656 => '1.20MB' and 1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if size < factor:
            return f"{size:.2f}{unit}{suffix}"
        size /= factor
