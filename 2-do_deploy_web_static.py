#!/usr/bin/python3
"""deploy archive for static deployment"""
from fabric.api import *
import os

env.hosts = ['52.204.227.199', '34.207.234.197']
env.user = 'ubuntu'
# env.key_filename = '~/.ssh/id_rsa'


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
