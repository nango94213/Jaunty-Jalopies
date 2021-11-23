import hashlib
import random
import string

class Hasher:
    staticmethod
    def _make_letter_salt():
        return ''.join([random.choice(string.ascii_letters) for x in range(10)])

    staticmethod
    def hash_pass(password, salt=None):
        if not salt:
            salt = Hasher._make_letter_salt()
        hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
        return f'{hash},.{salt}'

    staticmethod
    def check_hash(password, hash):
        salt = hash.split(',.')[1]
        if Hasher.hash_pass(password, salt) == hash:
            return True
        return