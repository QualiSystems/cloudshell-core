import base64
import os
from unittest import TestCase

from cloudshell.core.cryptography.aes_service import AESCipher


class TestAES(TestCase):

    def test_encrypt_decrypt(self):
        input = "test this"
        secret_key = base64.b64encode(os.urandom(16))
        cipher = AESCipher(secret_key)
        encrypted = cipher.encrypt(input)
        decrypted = cipher.decrypt(encrypted)
        self.assertTrue(input == decrypted)
