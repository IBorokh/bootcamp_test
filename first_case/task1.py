import hashlib


def task1(s="Python Bootcamp"):
    hash_dict = {'md5': hashlib.md5(s.encode()).hexdigest(),
                 'SHA1': hashlib.sha1(s.encode()).hexdigest(),
                 'with python "hash" func': hash(s)
                 }
    return hash_dict

