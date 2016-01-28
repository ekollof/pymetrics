#!/usr/bin/env python
"""
Deze module genereert shellcommando's die worden uitgevoerd op de host.
De functies genereren shell oneliners die meteen aan paramiko kunnen worden doorgegeven.
"""

import sys


def load(parameter=0):
    if parameter == 0:
        print 'FALSE: Invalid parameter'
        sys.exit(0)

    if int(parameter) > 3:
        print 'FALSE: Parameter out of range.'
        sys.exit(0)

    return 'value', "awk '{print $%d}' < /proc/loadavg" % (int(parameter) + 1)


def diskused(parameter='nodisk'):
    return 'disk', "df -kha /dev/%s | tail -n -1 | awk '{print $5}' | sed -e s/%%//" % parameter

def diskusedg(parameter='nodisk'):
    return 'disk', "df -ka /dev/%s | tail -n -1 | awk '{print $3 / 1024 / 1024}' | sed -e s/%%//" % parameter

def inodefree(parameter='nodisk'):
    return 'disk', '0'


def swapinuse(parameter=0):
    return 'value', '0'


def iops(parameter='nodisk'):
    return 'disk', '0'


def netload(parameter='nonic'):
    return 'nic', '0'

def test(parameter='test'):
    return 'test', 'OK'


if __name__ == '__main__':
    print "This does nothing."
    sys.exit(0)
