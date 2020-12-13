from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util import Padding
import string
import pyffx
from keys import get_token
alphabet = string.ascii_letters + string.digits + "!@#&$%^*"


def get_login_password(domain, password):
    token = get_token('/home/tides/token.txt')
    token = get_token()
    print(token)
    cipher = AES.new(token, AES.MODE_ECB)
    password = SHA256.new(data=password.encode()).hexdigest()[:16]
    session_key = cipher.encrypt(Padding.pad(domain.encode(), 64))
    cipher = pyffx.String(session_key, alphabet=alphabet, length=16)
    loginPassword = cipher.encrypt(password)
    return loginPassword


