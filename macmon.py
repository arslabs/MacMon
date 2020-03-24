#!/usr/bin/env python3

import os, sys, time
import io
import json
import subprocess
import serial
import serial_utils as su

def main():
    with open('config.json') as cfgFile:
        cfg = json.load(cfgFile)
#    print (cfg)

    print ("! Mac Monitor started.")

    vid = cfg["vid"]
    pid = cfg["pid"]
    serNo = cfg["serial_no"]
    dur = cfg["duration"]
    baud = cfg["baud"]

    dev = su.find_serial_dev_by_serNo(serNo)
    if dev == None:
        dev = su.find_serial_dev_by_vpid(vid, pid)
    if dev == None:
        print ("# Can not find display device")
        exit(-1)
    sp = su.openSerial(dev, baud)
    
    while 1:
        proc = subprocess.run(['istats', '--no-graph', '--value-only'], encoding='utf-8', stdout=subprocess.PIPE)
        result = proc.stdout.split('\n')
        r1 = b"%c,%.1f\n" % (b'T', float(result[1]))
        r2 = b"%c,%d\n" % (b'F', int(result[5]))

        sp.write(r1)
        time.sleep(0.001)
        sp.write(r2)

        time.sleep(dur)

if __name__=="__main__":
        main()

