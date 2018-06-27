#!/usr/bin/env python
# -*- coding: utf-8 -*-
__Auther__ = 'M4x'

from subprocess import Popen, PIPE
from sys import argv
import string

pinPath = "/home/m4x/pin-3.6-gcc-linux/pin"
pinInit = lambda tool, elf: Popen([pinPath, '-t', tool, '--', elf], stdin = PIPE, stdout = PIPE)
pinWrite = lambda cont: pin.stdin.write(cont)
pinRead = lambda : pin.communicate()[0]

if __name__ == "__main__":
    dic = map(chr, range(0x20, 0x80))
    idx = 0
    off = 0
    pwd = "_" * 28
    last = 0
    while True:
        pwd = pwd[: off] + dic[idx] + pwd[off + 1: ]
        pin = pinInit("./myInscount1.so", "./wyvern")
        pinWrite(pwd)

        now = int(pinRead().split("Count:")[1])
        print "input({}) -> ins({}) -> delta({})".format(pwd, now, now - last)
        last = now
        idx += 1


