import hashlib

class Md5:

    def __init__(self):
        pass

    def hash(self, obj):
        hash_object = hashlib.md5(obj.encode())
        return(hash_object.hexdigest())