#!/usr/bin/env python3

''' Remote Backup
'''

import os
import sys


def error(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def getConfig():
    try:
        with open("./rb.txt", 'r') as f:
            lines = f.readlines()
        host = None
        path = []
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] == '#':
                continue
            if host is None:
                host = line
            else:
                path.append(line)
        return [host, path]
    except FileNotFoundError:
        error(f"Config file not found!")


if __name__ == '__main__':
    [host, path] = getConfig()
    list = ' '.join(map(lambda s: f"'{s}'", path))
    cmd = '''rsync -aPR {host}:"{list}" .'''.format(
        host=host, list=list)
    print(cmd)
    os.system(cmd)
