#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import ascii_lowercase, digits
import os

allChars = digits + '_}' + ascii_lowercase

flag = 'ALEXCTF{'
wrong = '\x01\x01\x00\x00'
right = '\x00\x00\x01\x00'
case = '\x00\x00\x00\x00'

def tryFlag(f):
    os.system('(echo "{}" | ~/pin-3.6-gcc-linux/pin -t ./tracer.so -- ./move.unpacked) > /dev/null'.format(f))
    data = open('trace-1byte-writes.bin', 'rb').read()
    offset = len(f) * 4
    return data[offset - 4:offset]

while flag[:-1] != '}':
    for c in allChars:
        result = tryFlag(flag + c)
        if result == case:
            c = c.upper()
            result = tryFlag(flag + c)

        if result == right:
            flag += c
            print flag
            break
