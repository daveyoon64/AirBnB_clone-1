#!/usr/bin/python3
"""create archive for static deployment"""
from fabric.api import *
import tarfile
import os
from datetime import datetime, date, time

env.hosts = ['52.204.227.199', '34.207.234.197']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
        Distribute archive to webservers
    """
    if not os.path.isfile(archive_path):
        return None
    try:
        # put the file on the server
        file = archive_path[archive_path.find('web_static'):]
        serverpath = "/tmp/{}".format(file)
        put("{}".format(archive_path), "{}".format(serverpath))

        # extract the file
        folder = archive_path[archive_path.find('/')+1:archive_path.find('.')]
        whereto = '/data/web_static/releases/{}'.format(folder)
        run('sudo mkdir -p /data/web_static/releases/{}'.format(folder))
        run('sudo tar -xf {} -C {}'.format(serverpath, whereto))

        # delete archive, move files from folder/web_static to folder, delete
        run('sudo rm {}'.format(serverpath))
        run('sudo mv {}/web_static/* {}'.format(whereto, whereto))
        run('sudo rm -rf {}/web_static'.format(whereto))

        # delete the symlink and create a new one
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -sf {} /data/web_static/current'.format(whereto))
        print('New version deployed!')
    except:
        return False
    else:
        return True
