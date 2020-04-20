#!/usr/bin/env python3

import os, sys, time
import io
import json
import subprocess
import serial
import serial_utils as su
import paho.mqtt.client as mqtt

client = None

def main():
    with open('config.json') as cfgFile:
        cfg = json.load(cfgFile)
#    print (cfg)

    print ("! Mac Monitor started.")
    uart_enabled = cfg["uart_enabled"]
    mqtt_enabled = cfg["mqtt_enabled"]
    dur = cfg["duration"]

    if uart_enabled == 1:
        vid = cfg["vid"]
        pid = cfg["pid"]
        serNo = cfg["serial_no"]
        baud = cfg["baud"]

        dev = su.find_serial_dev_by_serNo(serNo)
        if dev == None:
            dev = su.find_serial_dev_by_vpid(vid, pid)
        if dev == None:
            print ("# Can not find display device")
            exit(-1)
        sp = su.openSerial(dev, baud)

    if mqtt_enabled == 1:
        broker = cfg["mqtt_broker"]
        port = cfg["mqtt_port"]
        topic1 = cfg["mqtt_topic1"]    
        topic2 = cfg["mqtt_topic2"]
        try:
            client = mqtt.Client("macmon")
            client.connect(broker, port=port)
        except:
            print ("# Can not connect to the mqtt broker")
            exit(-1)

    while 1:
        proc = subprocess.run(['istats', '--no-graph', '--value-only'], encoding='utf-8', stdout=subprocess.PIPE)
        result = proc.stdout.split('\n')

        if uart_enabled == 1:
            r1 = b"%c,%.1f\n" % (b'T', float(result[1]))
            r2 = b"%c,%d\n" % (b'F', int(result[5]))
            sp.write(r1)
            time.sleep(0.001)
            sp.write(r2)
        if mqtt_enabled == 1:
            temp = b"%.1f" % float(result[1])
            fan = b"%d" % int(result[5])
            client.publish(topic1, temp)
            client.publish(topic2, fan)

        time.sleep(dur)

if __name__=="__main__":
        main()
