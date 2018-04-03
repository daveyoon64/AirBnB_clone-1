#!/usr/bin/python3
"""create archive for static deployment"""
from fabric.api import *
import tarfile
import os
from datetime import datetime, date, time


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
    name = "versions/web_static_{}.tar.gz".format(ts)
    cmd = 'tar -zcvf {} web_static'.format(name)
    print("Packing web_static to {}".format(name))
    tar = local(cmd)
    if tar.failed:
        return None
    size = os.stat(name).st_size
    print('web_static packed: {} -> {}Bytes'.format(path, size))
    return name
