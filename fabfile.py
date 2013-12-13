#!/usr/bin/env python

"""
This is the fabric file. It handles calling our shell scripts, running shell commands,
and helping with general setup/cleanup.

Run 'fab --list' to see list of available commands.

References:
# http://docs.fabfile.org/en/1.0.1/usage/execution.html#how-host-lists-are-constructed
"""

# Asserting that your system python is in the general range of what we want
import platform
assert ('2', '6') <= platform.python_version_tuple() < ('3', '0')

from fabric.api import local


def run():
    """Kicks off your local server"""
    local('python runserver.py')
