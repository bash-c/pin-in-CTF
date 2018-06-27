#!/usr/bin/env python
# -*- coding: utf-8 -*-
__Auther__ = 'M4x' 

from z3 import *
from libnum import s2n
from itertools import permutations 
from ctypes import c_int32

table = '''FeVYKw6a0lDIOsnZQ5EAf2MvjS1GUiLWPTtH4JqRgu3dbC8hrcNo9/mxzpXBky7+\x00'''

def decodeBase64(src):
    delPaddingTail = {0: 0, 2: 4, 1: 2}
    value = ''
    n = src.count('=')
    sin = src[:len(src) - n]
    for c in sin:
        value += bin(table.find(c))[2:].zfill(6)
    value = value[:len(value) - delPaddingTail[n]]
    #  print value
    middle = []
    for i in range(8, len(value) + 1, 8):
        middle.append(int(value[i-8:i], 2))
    output = middle
    out =  hex(s2n(''.join(map(chr, output))))[2: -1]
    #  print out
    return out

m =[ 2, 2, 4, 4294967291, 1, 1, 3, 4294967293, 4294967295, 4294967294, 4294967293, 4, 4294967295, 0, 4294967294, 2 ]

#  m = [c_int32(i).value for i in m]
#  print m

f0 = lambda x: int(x, 16)
f1 = lambda x1, x2, x3, x4: (x1 * m[0] + x2 * m[1] + x3 * m[2] + x4 * m[3]) & 0xff
f2 = lambda x1, x2, x3, x4: (x1 * m[4] + x2 * m[5] + x3 * m[6] + x4 * m[7]) & 0xff
f3 = lambda x1, x2, x3, x4: (x1 * m[8] + x2 * m[9] + x3 * m[10] + x4 * m[11]) & 0xff
f4 = lambda x1, x2, x3, x4: (x1 * m[12] + x2 * m[13] + x3 * m[14] + x4 * m[15]) & 0xff

crypto = '''lUFBuT7hADvItXEGn7KgTEjqw8U5VQUq'''
key = decodeBase64(crypto)
print key
key = [f0(key[i: i + 2]) for i in range(0, len(key), 2)]
#  key = [key[i: i + 4] for i in range(0, len(key), 4)]
#  print key

s = Solver()
res = [BitVec(str(i), 16) for i in xrange(24)]
for i in res:
    s.add(And(i > 0, i < 256))
    
for i in xrange(6):
    s.add(f1(res[4 * i + 0], res[4 * i + 1], res[4 * i + 2], res[4 * i + 3]) == key[i * 4 + 0])
    s.add(f2(res[4 * i + 0], res[4 * i + 1], res[4 * i + 2], res[4 * i + 3]) == key[i * 4 + 1])
    s.add(f3(res[4 * i + 0], res[4 * i + 1], res[4 * i + 2], res[4 * i + 3]) == key[i * 4 + 2])
    s.add(f4(res[4 * i + 0], res[4 * i + 1], res[4 * i + 2], res[4 * i + 3]) == key[i * 4 + 3])


while s.check() == sat:
    #  print s.model()

    flag = ""
    for i in xrange(24):
        flag += chr(s.model()[res[i]].as_long() & 0xff)

    print flag
    s.add(res[0] != s.model()[res[0]])

else:
    print "Finish"

#  print flag
#  flag = []

#  dic = range(32, 127)[::-1]
#  for a in dic:
    #  for b in dic:
        #  for c in dic:
            #  for d in dic:
                #  if [f1(a, b, c, d), f2(a, b, c, d), f3(a, b, c, d), f4(a, b, c, d)] in key:
                    #  flag.append("".join(map(chr, (a, b, c, d))))

                #  if len(flag) == 6:
                    #  All = permutations(flag)
                    #  #  print All
                    #  for x, y, z, r, s, t in All:
                        #  t = x + y + z + r + s + t
                        #  if t.startswith("flag{") and t.endswith("}"):
                            #  print t
                    #  exit()
                    #  flag{dO_y0U_KNoW_0IlVm?}
