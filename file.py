"""
File utilities

License:
Copyright © 2017 The Climate Corporation
"""

import hashlib
import os

def length(f):
    """Get the length of a file"""
    f.seek(0, os.SEEK_END)
    length = f.tell()
    return length

def md5(f):
    """Get the md5 of a file's contents"""
    f.seek(0)
    md5 = hashlib.md5()
    chunk_size = 2**10

    for bytes_chunk in iter(lambda: f.read(chunk_size), b''):
        md5.update(bytes_chunk)

    return md5.hexdigest()
