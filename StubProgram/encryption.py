#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util import Padding
import string
import pyffx
import getpass
from keymanagement import get_token, valid_threshold
from utils import Encryption


alphabet = string.ascii_letters + string.digits + "!@#&$%^*"
username = getpass.getuser()


def get_login_password(domain, password):
    try:
        token = None
        #token = get_token("token.txt") # use this line if don't have usb
        #usb_token = None
        usb_token = get_token()
        token = usb_token or token
        print(token)
        if not valid_threshold(token):
            print("[-] Exceeds the secure threshold")
            exit(1)
        hash_pwd = SHA256.new(data=password.encode()).hexdigest()
        password = password + hash_pwd
        session_key = AES.new(token[12:], AES.MODE_ECB).encrypt(Padding.pad(domain.encode(), 128))
        cipher = pyffx.String(session_key, alphabet=alphabet, length=16)
        loginPassword = cipher.encrypt(password[:16])
        return loginPassword
    except:
        print("[-] Unexpected Error! Exit")
        exit(1)

if __name__ == "__main__":
    print(get_login_password("fb.com", "huythai"))

