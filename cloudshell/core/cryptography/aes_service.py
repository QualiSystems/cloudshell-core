import base64
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, key):
        self.key = base64.b64decode(key)

    def encrypt(self, raw):
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        raw = pad(raw)

        iv = Random.new().read(BS)

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        res = iv + cipher.encrypt(raw)
        return base64.b64encode(res)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        BS = 16
        iv = enc[:BS]
        unpad = lambda s: s[:-ord(s[-1])]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[BS:]))
