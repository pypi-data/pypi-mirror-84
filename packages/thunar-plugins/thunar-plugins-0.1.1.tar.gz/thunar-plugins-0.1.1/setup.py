#!/usr/bin/env python3
import sys
import subprocess
from setuptools import setup

# TODO: This is a really bulky solution... Rather use SCons here for example.
cmd = ["make", "-C", "thunar_plugins/locale"]
print("Running «{}»".format(" ".join(cmd)))
subprocess.check_output(cmd)

setup()
