import gzip
import os

def compress(file):
    """Wrapper for gzip.compress. Returns gzipped bytes of file"""
    return gzip.compress(file)

def decompress(file):
    """Wrapper for gzip.decompress. Returns decompressed bytes of file."""
    return gzip.decompress(file)

def check_and_rename(filename, add=0):
    """Returns incremented filename if name already taken."""
    original_file = filename
    if add != 0:
        split = os.path.splitext(filename)
        part_1 = split[0] + "_" + str(add)
        filename = "".join([part_1, split[1]])

    if not os.path.isfile(filename):
        return filename
    else:
        return check_and_rename(original_file, add+1)
