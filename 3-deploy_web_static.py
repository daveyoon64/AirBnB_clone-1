#!/usr/bin/python3
"""deploy archive for deployment"""
from fabric.api import *
import tarfile
import os
from datetime import datetime, date, time

env.hosts = ['52.204.227.199', '34.207.234.197']
env.user = 'ubuntu'
# env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """
        Gets the time, formats it, appends it, then packs web_static
    """
    try:
        os.makedirs('versions')
    except OSError as e:
        pass
    now = datetime.now()
    ts = now.strftime("%Y%m%d%H%M%S")
    name = "versions/web_static_{}.tgz".format(ts)
    cmd = 'tar -zcvf {} web_static'.format(name)
    print("Packing web_static to {}".format(name))
    tar = local(cmd)
    if tar.failed:
        return None
    size = os.stat(name).st_size
    print('web_static packed: {} -> {}Bytes'.format(path, size))
    return name


def do_deploy(archive_path):
    """
        Distribute archive to webservers
    """
    if os.path.isfile(archive_path):
        # put the file on the server
        filename = archive_path[archive_path.find('web_static'):]
        serverpath = "/tmp/{}".format(filename)
        put("{}".format(archive_path), "{}".format(serverpath))

        # extract the file
        folder = archive_path[archive_path.find('/')+1:archive_path.find('.')]
        whereto = '/data/web_static/releases/{}'.format(folder)
        run('mkdir -p /data/web_static/releases/{}'.format(folder))
        run('tar -xzf {} -C {}'.format(serverpath, whereto))

        # delete archive, move files from folder/web_static to folder, delete
        run('rm -rf {}'.format(serverpath))
        run('mv -n {}/web_static/* {}'.format(whereto, whereto))
        run('rm -rf {}/web_static'.format(whereto))

        # delete the symlink and create a new one
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(whereto))
        print('New version deployed!')
        return True
    return False


def deploy():
    """
        runs do_pack() and then do_deploy()
    """
    try:
        name = do_pack()
    except:
        return False
    value = do_deploy(name)
    return value
