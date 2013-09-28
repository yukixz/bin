#!/usr/bin/env python3
import getopt, sys
import math, os
from functools import reduce
from os.path import exists, isdir, isfile
from PIL import Image

EXTS = ['.bmp','.gif','.jpg','.jpeg','.png']
EXTS_MAP = {
    '.jpeg':'.jpg'
    }
USAGE = '''Usage: imgname.py [options...] directory
Options:
 -d dir     Destination directory.
 -q     Quiet mode, won't print Info messages.'''
SETTING_QUIET = False
SETTING_RENAME=True

def msg(level, text):
    if SETTING_QUIET and level=='II': return
    else: print("*%s* %s" % (level, text))


def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64
    hash = reduce(lambda x, a: x | (a[1] << a[0]),
                  enumerate([0 if i < avg else 1 for i in im.getdata()]),
                  0)
    return hex(hash)[2:].zfill(16)

def fix_ext(ext):
    try:    return EXTS_MAP[ext]
    except: return ext

def main(sdir, ddir=None):
    if not isdir(sdir):
        msg("EE","Source doesn't exist or isn't a directory.")
        return
    if not ddir: ddir=sdir
    elif not isdir(ddir):
        msg("EE","Destination doesn't exist or isn't a directory.")
        return
    
    msg("WW","In Src Directory: %s" % sdir)
    msg("WW","In Dst Directory: %s" % ddir)
    flist = os.listdir(sdir)
    for sname in flist:
        spath = os.path.join(sdir, sname)
        name = os.path.splitext(sname)[0]
        ext = os.path.splitext(sname)[1].lower()
        if not isfile(spath) or not ext in EXTS:
            continue
        
        dname = name + '.'+avhash(spath) + fix_ext(ext)
        dpath = os.path.join(ddir, dname)
        
        if spath==dpath:
            continue
        elif exists(dpath):
            msg("WW","%s => %s  FAIL! Destination exists." % (sname, dname))
        else:
            msg("II","%s => %s" % (sname.rjust(40), dname))
            if SETTING_RENAME:
                os.rename(spath, dpath)

if __name__ == '__main__':
    sdir=None
    ddir=None
    optlist, args = getopt.getopt(sys.argv[1:], 'd:qn')
    for key, value in optlist:
        if key=='-d': ddir=value
        if ket=='-n': SETTING_RENAME=False
        if key=='-q': SETTING_QUIET=True
    if args:
        sdir=args[0]
    
    if sdir: main(sdir, ddir)
    else: print(USAGE)
