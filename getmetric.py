#!/usr/bin/env python

import sys
import select
import imp
import paramiko
from pprint import pprint


def getcmd(metric, param):
    """
    Genereren van commando voor op de host.

    :param metric:
    :param param:
    :return:
    """

    # Laden van correcte metric functie
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
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, username='root', key_filename='key')
    stdin, stdout, stderr = ssh.exec_command(cmd)

    # commando gestuurd, antwoord ophalen.  Netjes wachten op uitvoer.
    output = ""
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            rs, ws, x1 = select.select([stdout.channel], [], [], 0.0)
            if len(rs) > 0:
                output = stdout.channel.recv(1024)

    ssh.close()

    return output


def result(host, cmd, param, vtype, treshold):
    """
    Uitvoeren van oneliner op remote host, en vergelijken met treshold

    :param host: Host waar informatie vandaan moet komen
    :param cmd: commando om uit te voeren
    :param vtype: type waarde die terug komt
    :param treshold: waarde waar informatie niet overheen mag.
    :return:
    """

    output = None

    if vtype == 'disk':
        # bestaat de mount wel?
        diskcmd = 'for i in "`lsblk -l | grep \'/\'`"; do echo $i | awk \'{print $1}\'; done'
        output = sshcmd(host, diskcmd)
        disks = output.split()
        print disks
        if param in disks:
            # gevonden
            output = sshcmd(host, cmd)
        else:
            print "FALSE: disk does not exist"
            sys.exit(0) # heeft geen zin om verder te gaan.

    if float(output) > float(treshold):
        return "TRUE: %s" % output
    else:
        return "FALSE: %s" % output


def main():
    """
    Main functie.

    :return:
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

    vtype, cmd = getcmd(metric, param)
    ret = result(host, cmd, param, vtype, treshold)

    print ret


if __name__ == '__main__':
    sys.exit(main())
