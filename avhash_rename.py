#!/usr/bin/env python3

import os
import sys
import getopt
import math
from functools import reduce
from PIL import Image


SUPPORTED_EXTS = ['.bmp', '.gif', '.jpg', '.png']
EXTS_MAP = {
    '.jpeg': '.jpg',
    }
DRY_RUN = False


def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64
    return reduce(lambda x, a: x | (a[1] << a[0]),
                  enumerate([0 if i < avg else 1 for i in im.getdata()]),
                  0)


def generate_name(path):
    im = Image.open(path)

    digest = avhash(im)
    digest_str = hex(digest)[2:].zfill(16)
    size = int(math.sqrt(im.size[0] * im.size[1]))
    size_str = hex(size % 0xFFFF)[2:].zfill(4)

    return digest_str + size_str


def fix_ext(ext):
    ext = ext.lower()
    return EXTS_MAP.get(ext, ext)


def main(files):
    for path in files:
        filedir = os.path.dirname(path)
        fileext = fix_ext(os.path.splitext(path)[1])
        if fileext not in SUPPORTED_EXTS:
            continue
        filename = generate_name(path)
        new_path = os.path.join(filedir, filename + fileext)

        if path == new_path:
            continue
        if os.path.exists(new_path):
            print("{src} -> {dst} failed!".format(src=path, dst=new_path))
            continue
        print("{src} -> {dst}".format(src=path, dst=new_path))
        if not DRY_RUN:
            os.rename(path, new_path)


if __name__ == '__main__':
    optlist, args = getopt.getopt(sys.argv[1:], 'n')
    for key, value in optlist:
        if key == '-n':
            DRY_RUN = True
    main(args)
