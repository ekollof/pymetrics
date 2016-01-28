#!/usr/bin/env python

import sys
import getmetric


def main():
    output = getmetric.sshcmd(sys.argv[1], sys.argv[2])
    print output

if __name__ == '__main__':
    sys.exit(main())
