#!/usr/bin/env python

import sys
import anydbm as dbm

def main():
    for k,v in dbm.open(sys.argv[1]).iteritems():
        print "key: {0:s} value: {1:s}".format(k, v)

if __name__ == '__main__':
    sys.exit(main())
