#!/usr/bin/python3
"""Directory deployer fabric module"""
from fabric.api import run, env, cd, put
from os.path import exists

env.user = 'ubuntu'
env.hosts = [
    '34.73.227.49',
    '35.173.250.239'
]


def do_deploy(archive_path):
    """Distribute .tgz archive to web servers.

    Args:
        archive_path (str): Path to archive to send.

    Returns:
        True if all operations are nominal, False if `archive_path` doesn't
        exists
    """
    if exists(archive_path):
        remote_releases_path = '/data/web_static/releases'
        archive_name = archive_path.split('/')[1]
        remote_dump_dir = archive_path.split('/')[1].split('.')[0]

        try:
            with cd('/tmp'):
                put(archive_path, '{}'.format(archive_name))

            run(
                'mkdir -p {}/{}'
                .format(
                    remote_releases_path,
                    remote_dump_dir
                )
            )
            run(
                'tar -xzf /tmp/{} -C {}/{}'
                .format(
                    archive_name,
                    remote_releases_path,
                    remote_dump_dir
                )
            )
            run(
                'rm -rf /tmp/{}'
                .format(
                    archive_name,
                )
            )
            run(
                'mv {}/{}/web_static/* {}/{}/'.format(
                    remote_releases_path,
                    remote_dump_dir,
                    remote_releases_path,
                    remote_dump_dir,
                )
            )
            run(
                'rm -rf {}/{}/web_static'
                .format(
                    remote_releases_path,
                    remote_dump_dir
                )
            )
            run('rm -rf /data/web_static/current')
            run(
                'ln -s {}/{} /data/web_static/current'
                .format(
                    remote_releases_path,
                    remote_dump_dir
                )
            )
        except Exception:
            return False
        return True
    return False
