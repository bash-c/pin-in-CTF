#!/usr/bin/env python
# -*- coding: utf-8 -*-
__Auther__ = 'M4x'

from subprocess import Popen, PIPE
import string
from sys import argv

pinPath = "/home/m4x/pin-3.6-gcc-linux/pin"

def getLen():
    last = 0
    for i in xrange(50):
        pin = Popen([pinPath, '-t', './myInscount1.so', '--', './re'], stdin = PIPE, stdout = PIPE)
        pin.stdin.write('_' * i + '\n')
        out, err = pin.communicate()
        now = int(out.split('Count')[1])
        delta = now - last
        print "inputLen({}) -> int({}) -> delta({})".format(i, now, delta)
        if delta > 10000 and i:
            print "\n[*]Possible length -> {}\n".format(i)
            return i
        last = now

if __name__ == "__main__":
    pLen = getLen()
