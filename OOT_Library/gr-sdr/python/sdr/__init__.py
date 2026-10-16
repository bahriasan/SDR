#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio SDR module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the sdr namespace
try:
    # this might fail if the module is python-only
    from .sdr_python import *
except ModuleNotFoundError:
    pass

# import any pure python here
from .cst_pattern import cst_pattern
from .aoa_estimator import aoa_estimator
from .aoa_visualizer_3d import aoa_visualizer_3d
from .udp_aoa_sender import udp_aoa_sender
#
