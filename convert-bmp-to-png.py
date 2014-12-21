#!/usr/bin/env python3

import os
import sys
import getopt

try:
    from PIL import Image
except ImportError:
    print("Cannot not find PIL.\nYou can download Pillow from https://pypi.python.org/pypi/Pillow/")
    sys.exit(1)


if __name__ == '__main__':
    DRY_RUN = False

    optlist, args = getopt.getopt(sys.argv[1:], 'n')
    for key, value in optlist:
        if key == '-n':
            DRY_RUN = True

    for path in args:
        filename, fileext = os.path.splitext(path)
        fileext = fileext.lower()

        if fileext in ['.bmp']:
            newpath = filename + '.png'
            print("%s -> %s" % (path, newpath))
            if not DRY_RUN:
                im = Image.open(path)
                im.save(newpath)



