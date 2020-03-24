from serial.tools import list_ports
import serial

def find_serial_dev_by_serNo(serNo):
  sl = list(list_ports.comports())
  for s in sl:
    if s.serial_number == serNo:
      return s.device
  return None

def find_serial_dev_by_vpid(vid, pid):
  sl = list(list_ports.comports())
  for s in sl:
    if (s.pid == pid) and (s.vid == vid):
      return s.device
  return None

def openSerial(device, bps):
  try:
    s = serial.Serial(device, bps)
  except serial.SerialException:
    print ("# openSerial: device is busy or no device")
    return None
  except ValueError:
    print ("# openSerial: value error")
    return None
  return s

