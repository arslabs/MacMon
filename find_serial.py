#!/usr/bin/env python3

from serial.tools import list_ports

sl = list(list_ports.comports())
for s in sl:
  print (str(s) + ", vid: " + str(s.vid) + ", pid: " + str(s.pid) + ", serial no.: " + str(s.serial_number))
