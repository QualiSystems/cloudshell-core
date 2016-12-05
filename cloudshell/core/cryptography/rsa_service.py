import base64
import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


class RsaService(object):
    def __init__(self):
        pass

    @staticmethod
    def read_public_key():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_full_name = os.path.join(dir_path, "rsa_key.txt")
        file_object = open(file_full_name)
        return file_object.read()

    def encrypt(self, input):
        public_key_text = RsaService.read_public_key()
        public_key = RSA.importKey(public_key_text)
        rsa_cipher = PKCS1_v1_5.new(public_key)
        return base64.b64encode(rsa_cipher.encrypt(input))
