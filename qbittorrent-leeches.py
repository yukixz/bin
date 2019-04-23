#!/usr/bin/env python3
import json
import re
import requests
from urllib.parse import urljoin

SID='YOUR_SID'
BASE='http://127.0.0.1:8112'
CACHE='/tmp/qbittorrent-leeches.txt'
BANCLIENT=re.compile(r'(-XL0012-)|(Xunlei)|(^7\.)|(QQDownload)', re.I)

# 0. Load banned IPs
banips = []
try:
    with open(CACHE, 'r') as f:
        banips.extend(f.read().splitlines())
except FileNotFoundError:
    pass

# 1. Get torrent list
resp = requests.get(urljoin(BASE, '/api/v2/torrents/info'), params={ 'filter': 'active' }, cookies={ 'SID': SID })
torrents = resp.json()

# 2. Get torrent peers data
peers = {}
for t in torrents:
    resp = requests.get(urljoin(BASE, '/api/v2/sync/torrentPeers'), params={ 'hash': t['hash'] }, cookies={ 'SID': SID })
    body = resp.json()
    peers.update(body['peers'])

# 3. Detect ban IP
for p, a in peers.items():
    if BANCLIENT.match(a['client']):
        banips.append(a['ip'])
with open(CACHE, 'w') as f:
    f.write('\n'.join(banips))

# 4. Set preferences
banips = banips[-1000:-1]
resp = requests.post(urljoin(BASE, '/api/v2/app/setPreferences'), cookies={ 'SID': SID }, data={
    'json': json.dumps({
        'ip_filter_enabled': True,
        'banned_IPs': '\n'.join(banips),
    }, separators=(',', ':'))
})
