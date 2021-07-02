#!/usr/bin/env python3

import hashlib
import os


class FileMetadata:

    def __init__(self, path):
        self.path = os.path.realpath(os.path.expanduser(path))
        self.get_attributes()

    def get_attributes(self):
        self.get_shasum()
        self.get_filesize()

    def get_shasum(self):
        sha256_hash = hashlib.sha256()
        with open(self.path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b''):
                sha256_hash.update(byte_block)
            self.shasum = sha256_hash.hexdigest()

    def get_filesize(self):
        self.filesize = os.path.getsize(self.path)
