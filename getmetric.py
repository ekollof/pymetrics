#!/usr/bin/env python

import os
import sys
import anydbm as dbm
import select
import imp
import paramiko
from pprint import pprint


def getcmd(metric, param):
    """
    Generate command for the target host

    :param metric:
    :param param:
    :return:
    """

    # Load correct metric function from lib/mtype.py

    m = imp.load_source('mtype', 'lib/mtype.py')
    if hasattr(m, metric):
        mtype = getattr(m, metric)
        vtype, cmd = mtype(param)
    else:
        print "FALSE (metric does not exist yet. Typo?)"
        allmods = []
        for mod in dir(m):
            if mod.startswith('_') or mod == "sys":
                continue
            allmods.append(mod)
            sys.stderr.write("Valid metrics:\n\t")
            pprint(allmods)
            sys.exit(0)

    return vtype, cmd


def sshcmd(host, cmd):
    """
        Execute command on host using Paramiko
    """
    ssh = paramiko.SSHClient()

    # This avoids the missing host key prompt.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # TODO: We might want to put this in a config file. Hardcoding is not nice.
    ssh.connect(host, 22, username='root', key_filename='key')

    stdin, stdout, stderr = ssh.exec_command(cmd)

    # Sent command, fetch answer. Wait for EOF.

    output = ""
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            rs, ws, x1 = select.select([stdout.channel], [], [], 0.0)
            if len(rs) > 0:
                output = stdout.channel.recv(1024)

    ssh.close()

    return output


def result(host, cmd, param, vtype, treshold, metric, cache):
    """
    Execute a oneliner on remote host and check treshold.

    :param host: Host to check on
    :param cmd: commando we need to execute
    :param vtype: value type (so we know what to do with it)
    :param treshold: Treshold value
    :return:
    """

    output = None

    # TODO: Exception for disks. Maybe not the correct place.
    if vtype == 'disk':
        # bestaat de mount wel?
        diskcmd = 'lsblk -l | grep / | awk \'{print $1}\''
        output = sshcmd(host, diskcmd)
        disks = output.split()
        #print disks
        if param in disks:
            # gevonden
            output = sshcmd(host, cmd)
        else:
            print "FALSE: disk does not exist"
            sys.exit(0)  # No use continuing.


    if vtype == 'discover':
        output = sshcmd(host, cmd).splitlines(True)
        print output

        for line in output:
            if line.startswith('NET: '):
                netdev = line[5:]
                print netdev

    return "TRUE: Discovery done"

    if vtype == 'value':
        output = sshcmd(host, cmd)
        output = output.strip()

    cache[host + '-' + metric + '-' + vtype + '-' + param] = output

    if float(output) > float(treshold):
        return "TRUE: %s" % output
    else:
        return "FALSE: %s" % output


def main():
    """
    Main
    """

    if len(sys.argv) < 2:
        print "%s <host> <metric type> <parameter> <treshold>" % sys.argv[0]
        sys.exit(0)

    if len(sys.argv) < 4:
        print "Not enough arguments."
        sys.exit(0)

    host = sys.argv[1]
    metric = sys.argv[2]
    param = sys.argv[3]
    treshold = sys.argv[4]

    # Init lokale cache
    cache = dbm.open(os.path.expanduser('~') + '/metricscache.dbm', 'c')

    vtype, cmd = getcmd(metric, param)
    ret = result(host, cmd, param, vtype, treshold, metric, cache)

    cache.close()

    print ret


if __name__ == '__main__':
    sys.exit(main())
