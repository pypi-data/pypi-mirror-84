# -*- coding: utf-8 -*-
"""Print system information."""

import platform
import sys
from os import environ

import click
from tabulate import tabulate

from pype.constants import ENV_CONFIG_FOLDER
from pype.util.cli import fname_to_name


@click.command(name=fname_to_name(__file__), help=__doc__)
def main():
    """Script's main entry point."""
    unset = 'Not set'
    print('PYPE SYSTEM ENVIRONMENT')
    infos = [
        ['MACHINE', platform.machine()],
        ['PROCESSOR', platform.processor()],
        ['PLATFORM', platform.platform()], ['VERSION', platform.version()],
        ['RELEASE', platform.release()], ['SYSTEM', platform.system()],
        ['PY VERSION', sys.version], ['PY VERSION_INFO', sys.version_info],
        ['SHELL', environ.get('SHELL', unset)],
        ['CONFIG FOLDER', environ.get(ENV_CONFIG_FOLDER, unset)]
    ]
    print(tabulate(infos))
