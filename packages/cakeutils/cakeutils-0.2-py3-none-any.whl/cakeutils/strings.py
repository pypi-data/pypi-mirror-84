#! /usr/bin/env python

## This file is part of cakeutils
## See http://www.secdev.org/projects/cakeutils for more informations
## Copyright (C) Philippe Biondi <phil@secdev.org>
## This program is published under a GPLv2 license


# This file contains string manipulation functions


def strxor(a, b):
    "returns a^b, byte by byte. Shorter string wraps"
    la = len(a)
    lb = len(b)
    return "".join(chr(ord(a[i%la])^ord(b[i%lb])) for i in range(max(la,lb)))

def stradd(a, b):
    "returns (a+b)%256, byte by byte. Shorter string wraps"
    la = len(a)
    lb = len(b)
    return "".join(chr((ord(a[i%la])+ord(b[i%lb]))%256) for i in range(max(la,lb)))

def strsub(a, b):
    "returns (a-b)%256, byte by byte. Shorter string wraps"
    la = len(a)
    lb = len(b)
    return "".join(chr((ord(a[i%la])-ord(b[i%lb]))%256) for i in range(max(la,lb)))



def printable(x):
    "replace non-printable characters by '.'"
    return "".join(c if  (32 <= ord(c) <=  127) else "." for c in x) 


def linehex(x):
    return " ".join("%02x" % ord(c) for c in x)

def linehexdump(x):
    return "%s  %s" % (" ".join("%02x" % ord(c) for c in x), printable(x))



def hexdump(x):
    x=str(x)
    l = len(x)
    i = 0
    while i < l:
        print("%04x  " % i, end=' ')
        for j in range(16):
            if i+j < l:
                print("%02X" % ord(x[i+j]), end=' ')
            else:
                print("  ", end=' ')
            if j%16 == 7:
                print("", end=' ')
        print(" ", end=' ')
        print(printable(x[i:i+16]))
        i += 16

def shexdump(x):
    s = []
    x=str(x)
    l = len(x)
    i = 0
    while i < l:
        line = "%04x   " % i
        for j in range(16):
            if i+j < l:
                line += "%02X " % ord(x[i+j])
            else:
                line += "   "
            if j%16 == 7:
                line += " "
        line += "  "
        line += printable(x[i:i+16])
        s.append(line)
        i += 16
    return "\n".join(s)

