#!/usr/bin/env python
"""
This module holds shell commands that will be executed on the host. They will
be handed over to the getmetrics program. This file is dynamically parsed. Just
add your defs in here and getmetrics should just pick them up.
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
    return 'disk', "df -kha  | %s | tail -n -1 | awk '{print $5}' | sed -e s/%%//" % parameter

def diskusedg(parameter='nodisk'):
    return 'disk', "df -ka | grep %s | tail -n -1 | awk '{print $3 / 1024 / 1024}' | sed -e s/%%//" % parameter

def inodefree(parameter='nodisk'):
    return 'disk', '0'

def swapinuse(parameter=0):
    return 'value', '0'

def iops(parameter='nodisk'):
    return 'disk', '0'

def netload(parameter='nonic'):
    return 'nic', '0'

def test(parameter='test'):
    return 'test', 'uname -a'

def discover(parameter=0):
    return 'discover', 'ifconfig -s | tail -n +2 | awk \'{print $1}\' | xargs echo -e NET: && lsblk -l | grep / | awk \'{print $1}\' | xargs echo DISK:'

def compare(parameter=0):
    return 'compare',  'ifconfig -s | tail -n +2 | awk \'{print $1}\' | xargs echo -e NET: && lsblk -l | grep / | awk \'{print $1}\' | xargs echo DISK:'

if __name__ == '__main__':
    print "This does nothing."
    sys.exit(0)
