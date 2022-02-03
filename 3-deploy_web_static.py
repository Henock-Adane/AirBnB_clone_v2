#!/usr/bin/python3
"""Directory deployer fabric module"""
from fabric.api import run, env, cd, put, local, task, execute, hosts
from os.path import exists

env.hosts = [
    '34.73.227.49',
    '35.173.250.239'
]


@task
def do_pack():
    """Pack `web_static` directory to .tgz inside versions.

    Returns:
        path of archive <class 'str'> or
        None <class 'NoneType'> upon an exception
    """
    try:
        timestamp = local("date +%Y%m%d%H%M%S", capture=True)
        archive_name = 'web_static_{}.tgz'.format(timestamp)

        local("mkdir -p versions;")
        print(
            'Packing web_static to /versions/{}'
            .format(timestamp)
        )
        local(
            "tar -cvzf versions/{} web_static"
            .format(archive_name)
        )
        print(
            '`{}` archive successfully created!'
            .format(archive_name)
        )
        return 'versions/{}'.format(archive_name)
    except Exception:
        return None


@task
def do_deploy(archive_path):
    """Deploy .tgz archive to web servers.

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
                'mv {0}/{1}/web_static/* {0}/{1}/'.format(
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
            print('New version deployed!')
        except Exception:
            return False
        return True
    return False


@task
@hosts('34.73.227.49')
def deploy():
    """Pack and deploy web_static to servers

    Returns:
        True if all operations are nominal, False otherwise
    """
    path = do_pack()
    if path:
        deployed = execute(
            do_deploy,
            path,
            hosts=['34.73.227.49', '35.173.250.239']
        )
        return deployed['34.73.227.49'] and deployed['35.173.250.239']
    return False
