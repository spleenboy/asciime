#! /usr/bin/python
from array import array

size = 9
for i in range( 0, 513 ):
    n = bin(i).replace("0b", "").zfill(size)
    print "[ %s, %s, %s," % (n[0], n[1], n[2])
    print "  %s, %s, %s," % (n[3], n[4], n[5])
    print "  %s, %s, %s, ], [ ]," % (n[6], n[7], n[8])
