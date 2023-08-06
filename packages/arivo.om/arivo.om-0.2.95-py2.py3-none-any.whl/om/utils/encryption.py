import json
import logging
import os
import threading

import gnupg
from redis import StrictRedis

from om.utils import config

_encryption = threading.local()


def get_encryption():
    global _encryption
    if not hasattr(_encryption, "val"):
        _encryption.val = Encryption()
    return _encryption.val


def encrypt(data, outfile=None, compress=True, key_name="default"):
    return get_encryption().encrypt(data, outfile, compress, key_name)


def encrypt_file(file_name, out_file_name=None, key_name="default"):
    return get_encryption().encrypt_file(file_name, out_file_name=out_file_name, key_name=key_name)


class Encryption:
    keys = {}
    fingerprints_by_key_name = {}
    REDIS_HKEY = "kv"
    REDIS_KEY_PREFIX = "encryption_key-"
    REDIS_DEFAULT_KEY = "encryption_key-default"

    def __init__(self):
        self.redis = StrictRedis(host=config.string("REDIS_HOST", "localhost"),
                                 port=config.int("REDIS_PORT", 6379),
                                 db=config.int("REDIS_DB", 0))
        self.gpg = gnupg.GPG()
        self.gpg.encoding = 'utf-8'
        self.lock = threading.RLock()
        self.used_fingerprints = {}
        self.old_fingerprints = []
        self.init_keys()

    def init_keys(self):
        keys = [x for x in self.redis.hgetall("kv").keys() if x.startswith(b"encryption_key-")]
        for key in keys:
            key_name = key.decode("utf-8").split("-", 1)[1]
            fp = self.get_fingerprint(key_name)
            self.cleanup(fp)

        fingerprints_to_delete = [x["fingerprint"] for x in self.gpg.list_keys()
                                  if x["fingerprint"] not in list(self.fingerprints_by_key_name.values())]
        # remove all unnecessary keys from keyring
        for fp in fingerprints_to_delete:
            self.gpg.delete_keys(fp)

    def cleanup(self, fp):
        if fp:
            with self.lock:
                self.used_fingerprints[fp] -= 1
                self.remove_old_key(fp)

    def remove_old_key(self, fp):
        if fp in self.old_fingerprints and not self.used_fingerprints[fp]:
            self.gpg.delete_keys(fp)
            del self.used_fingerprints[fp]
            self.old_fingerprints.remove(fp)

    def get_fingerprint(self, key_name="default"):
        redis_key = self.REDIS_KEY_PREFIX + key_name
        data = self.redis.hget(self.REDIS_HKEY, redis_key)

        with self.lock:
            if data:
                new_key = json.loads(data)

                if not new_key.get("fingerprint"):
                    self.redis.hdel(self.REDIS_HKEY, redis_key)
                    return None

                # new key, fingerprint_id for backwards compatibility
                if (new_key.get("fingerprint") or new_key.get("fingerprint_id")) != self.fingerprints_by_key_name.get(
                        key_name):
                    old_fingerprint = self.fingerprints_by_key_name.get(key_name)

                    import_result = self.gpg.import_keys(new_key["pubkey"])
                    if import_result.unchanged or import_result.imported:
                        fp = import_result.fingerprints[0]
                        # multiple fingerprints?
                        if any(x != fp for x in import_result.fingerprints):
                            return None
                        self.fingerprints_by_key_name[key_name] = fp
                        self.used_fingerprints[fp] = 0
                        if old_fingerprint:
                            self.old_fingerprints.append(old_fingerprint)
                            self.remove_old_key(old_fingerprint)
            # delete key from key ring, no longer here
            else:
                old_fingerprint = self.fingerprints_by_key_name[key_name]
                self.old_fingerprints.append(old_fingerprint)
                self.remove_old_key(old_fingerprint)

            fp = self.fingerprints_by_key_name.get(key_name)
            if fp:
                self.used_fingerprints[fp] += 1
            return fp

    def encrypt_file(self, file_name, out_file_name=None, key_name="default"):
        new_name = out_file_name or f"{file_name}.pgp"
        if not new_name.endswith(".pgp"):
            new_name = new_name + ".pgp"

        with open(file_name, "rb") as file:
            compress = True
            ending = file_name.rsplit(".", 1)
            if ending in ["gz", "jpg", "jpeg"]:
                compress = False

            success = self.encrypt(file, new_name, compress, key_name)
        if success and False:
            os.remove(file_name)
            return True
        return False

    def encrypt(self, data, out_file=None, compress=True, key_name="default"):
        if out_file is not None and not out_file.endswith(".pgp"):
            out_file += ".pgp"

        extra_args = ['-z', '0']
        if compress:
            extra_args = None

        fp = self.get_fingerprint(key_name)
        if not fp:
            return None

        if isinstance(data, str) or isinstance(data, bytes) or isinstance(data, bytearray):
            result = self.gpg.encrypt(data, fp, always_trust=True, extra_args=extra_args, output=out_file)
        else:
            result = self.gpg.encrypt_file(data, fp, always_trust=True, extra_args=extra_args, output=out_file)
        self.cleanup(fp)

        if not result.ok:
            logging.warning(f"Decryption error {result.status}")
            return None
        return result.data

    def decrypt(self, data):
        if isinstance(data, str) or isinstance(data, bytes) or isinstance(data, bytearray):
            decrypted = self.gpg.decrypt(data)
        else:
            decrypted = self.gpg.decrypt_file(data)
        if decrypted.ok:
            return decrypted.data
        return None
