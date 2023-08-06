"""
Other similar libraries:
https://pypi.org/project/rocksdbdict/
"""
import rocksdb
import gc

# Good samples here:
# https://github.com/adammarples/rocksdbdict/blob/master/rocksdbdict.py


def utf_to_bytes(s):
    return s.encode('utf-8')


def decode_utf(s):
    return s.decode('utf-8')


class SimpleRocks(object):

    def __init__(
            self, path, read_only=False, create_if_missing=True,
            key_encode=utf_to_bytes,
            val_encode=utf_to_bytes,
            key_decode=decode_utf,
            val_decode=decode_utf
    ):
        self.path = path
        self.db = rocksdb.DB(path, rocksdb.Options(create_if_missing=create_if_missing), read_only=read_only)
        self.key_encode = key_encode
        self.val_encode = val_encode
        self.key_decode = key_decode
        self.val_decode = val_decode
        self.closed = False

    def __contains__(self, key_):
        return self.get(key_) is not None

    def __del__(self):
        if self.db is not None:
            del(self.db)
            self.db = None
            gc.collect()

    def __setitem__(self, key, value):
        self.put(key, value)

    def __getitem__(self, key_):
        val = self.get(key_)
        if val is None:
            raise KeyError(f'{key_} not in {self}')
        return val

    def __delitem__(self, key):
        byteskey = self.key_encode(key)
        self.db.delete(byteskey)

    def put(self, k, v):
        assert not self.closed
        self.db.put(self.key_encode(k), self.val_encode(v))

    def get(self, k):
        assert not self.closed
        val = self.db.get(self.key_encode(k))
        if val is None:
            return val
        return self.val_decode(val)

    def close(self):
        # we need to do this b/c rocks will crash frequently on jupyter
        del(self.db)
        self.db = None
        self.closed = True
        gc.collect()

    def __repr__(self):
        return f'SimpleRocks<{self.path}>'
