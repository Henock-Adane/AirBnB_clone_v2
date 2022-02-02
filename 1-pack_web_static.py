#!/usr/bin/python3
"""Directory packer fabric module"""
from fabric.api import local


def do_pack():
    """Pack `web_static` directory to .tgz inside versions."""

    name = local("date +%Y%m%d%H%M%S", capture=True)
    local("mkdir -p versions;", capture=True)
    local(
        "tar -cvzf versions/web_static_{}.tgz web_static".format(name),
    )
