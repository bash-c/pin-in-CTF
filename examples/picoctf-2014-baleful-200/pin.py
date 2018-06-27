#!/usr/bin/env python
# -*- coding: utf-8 -*-
__Auther__ = 'M4x'

from subprocess import Popen, PIPE
from sys import argv
import IPython
import pdb
import string

pinPath = "/home/m4x/pin-3.6-gcc-linux/pin"
pinInit = lambda tool, elf: Popen([pinPath, '-t', tool, '--', elf], stdin = PIPE, stdout = PIPE)
pinWrite = lambda cont: pin.stdin.write(cont)
pinRead = lambda : pin.communicate()[0]

if __name__ == "__main__":
    #  last = 0
    #  for i in xrange(1, 50):
        #  pin = pinInit("./myInscount1.so", "./baleful")
        #  pinWrite('_' * i)
        #  now = int(pinRead().split(':')[1])
        #  print "inputLen({}) -> ins({}) -> delta({})".format(i, now, now - last)

        #  if now - last > 2000 and last:
            #  exit()
        #  last = now

    pwd = "_" * 30
    off = 0
    idx = 0
    #  dic = map(chr, xrange(0x20, 0x80))
    dic = map(chr, xrange(94, 123))

    last = 0
    while True:
        pin = pinInit("./myInscount1.so", "./baleful_unpacked")
        #  if off == 1:
            #  pdb.set_trace()
        pwd = pwd[: off] + dic[idx] + pwd[off + 1:]
        #  print pwd
        pinWrite(pwd + '\n')
        now = int(pinRead().split(':')[1])
        print "input({}) -> ins({}) -> delta({})".format(pwd, now, now - last)

        if now - last < 0:
            print pwd
            off += 1
            if off >= 30:
                break
            idx = 0
            last = 0
            continue

        idx += 1
        last = now
