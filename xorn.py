#!/usr/bin/env python3

import struct
import sys

def main(files):
    for path in files:
        with open(path, 'r+b') as f:
            rbuffer = f.read(SIZE)
            wbuffer = b""

            if len(rbuffer) != SIZE:
                continue
            while len(rbuffer) > 0:
                wbuffer += struct.pack('=Q',
                        struct.unpack('=Q', rbuffer[:8])[0] ^ MAGIC_NUMBER)
                rbuffer = rbuffer[8:]

            f.seek(0)
            f.write(wbuffer)


if __name__ == '__main__':
    config = {
            'SIZE': 64, # Must be a Multiple pf 8.
            'MAGIC_NUMBER': 0x0123456789ABCDEF, # Must be 8 bytes
            }
    main(files=sys.argv[1:], **config)
