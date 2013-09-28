#!/usr/bin/env python3

import os
import sys
from os.path import exists, isdir, isfile


from functools import reduce
from PIL import Image

def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64
    hash = reduce(lambda x, a: x | (a[1] << a[0]),
                  enumerate([0 if i < avg else 1 for i in im.getdata()]),
                  0)
    return hex(hash)[2:].zfill(16)


if __name__ == '__main__':
    EXTS = ['.bmp','.gif','.jpg','.jpeg','.png']
    for path in sys.argv[1:]:
        ext = os.path.splitext(path)[1].lower()
        if isfile(path) and ext in EXTS:
            print(avhash(path))
