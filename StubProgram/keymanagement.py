#!/usr/bin/env python3

import os
import string
import random
import io
import time
from utils import Encryption, get_mount_points, get_serial_number


def get_token(file_path=None):
    usb_token_path = ""
    if get_mount_points() != []:
        usb_token_path = get_mount_points()[0] + "/token.txt"

    file_path = file_path or usb_token_path

    if not os.path.exists(file_path):
        generate_key(file_path)

    file = open(file_path, 'rb')
    token = file.read()
    print(token)
    token = Encryption.decrypt(get_serial_number().encode(), token)
    update_token(file_path, token)
    return token


def generate_key(file_path):
    lastaccss = str(int(time.time())).encode()
    freq = b"10"
    key = bytes([random.randrange(0, 256) for _ in range(32)])
    token = Encryption.encrypt(get_serial_number().encode(), lastaccss + freq + key)
    file = open(file_path, 'wb')
    file.write(token)


def update_token(file_path, token):
    lastaccess = int(token[:10])
    freq = int(token[10:12])
    lastaccess, freq = modify_threshold(lastaccess, freq)
    key = token[12:]
    token = Encryption.encrypt(get_serial_number().encode(), str(lastaccess).encode() + str(freq).encode() + key)
    file = open(file_path, 'wb')
    file.write(token)


def valid_threshold(token):
    lastaccess = int(token[:10])
    freq = int(token[10:12])
    timestamp = int(time.time())
    if timestamp - lastaccess < 5 * 60 and freq > 20:
        return False
    return True

def modify_threshold(lastaccess, freq):
    timestamp = int(time.time())
    if timestamp - lastaccess > 5 * 60:
        freq = 10;
        lastaccess = timestamp 
    else: freq += 1
    return lastaccess, freq


if __name__ == '__main__':
    #print(list(get_usb_devices().values())[0])
    #get_timestamp('token.txt')
    #generate_key("token.txt")
    #print(get_usb_devices())
    #print(get_serial_number())
    #print(get_token('token.txt'))
    pass
