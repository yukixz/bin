#!/usr/bin/env python3

''' Remove Backup
'''

import os

# Config
HOST = "rainbow.dazzyd.org"
FILES = [
    # SSH
    "/etc/ssh/sshd_config",
    # DNS
    "/etc/named.conf",
    "/var/named/dazzyd.org.zone",
    # HTTP & HTTPS
    "/etc/nginx/conf.d/dazzyd.conf",
    "/etc/nginx/nginx.conf",
    # LetsEncrypt
    "/etc/letsencrypt/",
    "/etc/cron.monthly/certbot",
]


if __name__ == '__main__':
    files = map(lambda x: "'{}'".format(x), FILES)
    cmd = '''rsync -aPR {host}:"{list}" .'''.format(
        host=HOST,
        list=' '.join(files))
    os.system(cmd)
