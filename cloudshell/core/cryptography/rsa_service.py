import os


class RsaService(object):
    def __init__(self):
        pass

    @staticmethod
    def read_public_key():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_full_name = os.path.join(dir_path, "rsa_key.txt")
        file_object = open(file_full_name)
        return file_object.read()
