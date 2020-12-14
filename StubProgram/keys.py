#!/usr/bin/env python

import os
from glob import glob
from subprocess import check_output, CalledProcessError
import string
import random

def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)


def get_mount_points(devices=None):
    devices = devices or get_usb_devices()  # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines()
    output = [tmp.decode('UTF-8') for tmp in output]

    def is_usb(path):
        return any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    return [info.split()[2] for info in usb_info]


def get_token(file_path=None):
    try:
        usb_token_path = ""
        if get_mount_points() != []:
            usb_token_path = get_mount_points()[0] + "/token.txt"

        file_path = file_path or usb_token_path

        if not os.path.exists(file_path):
            generate_key(file_path)

        file = open(file_path, 'rb')
        token = file.readline()
        return token
    except: 
        return ""


def generate_key(file_path):
    file = open(file_path, 'wb')
    token = bytes([random.randrange(0, 256) for _ in range(32)])
    file.write(token)

if __name__ == '__main__':
    print(get_mount_points())