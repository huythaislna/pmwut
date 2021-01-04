from Crypto.Cipher import AES
from Crypto.Util import Padding
import usb
import os
from glob import glob
from subprocess import check_output, CalledProcessError

class Encryption:
    def encrypt(key, value):
        cipher = AES.new(Padding.pad(key,32), AES.MODE_ECB)
        return cipher.encrypt(Padding.pad(value,64))

    def decrypt(key, value):
        cipher = AES.new(Padding.pad(key, 32), AES.MODE_ECB)
        return Padding.unpad(cipher.decrypt(value), 64)


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


def get_serial_number():
    try:
        path = list(get_usb_devices().values())[0]
        bus_port = path.split('/')[6]
        bus, port = bus_port.split('-')
        dev = usb.core.find(bus=int(bus), port_number=int(port))
        return dev.serial_number
    except:
        print("Can't get serial number")
        exit(1)

def welcome():
    print("""
 _______  ____    ____  ____      ____  _____  _____  _________  
|_   __ \|_   \  /   _||_  _|    |_  _||_   _||_   _||  _   _  | 
  | |__) | |   \/   |    \ \  /\  / /    | |    | |  |_/ | | \_| 
  |  ___/  | |\  /| |     \ \/  \/ /     | '    ' |      | |     
 _| |_    _| |_\/_| |_     \  /\  /       \ \__/ /      _| |_    
|_____|  |_____||_____|     \/  \/         `.__.'      |_____|  created by F2

        """)



if __name__ == "__main__":
    print(get_serial_number())