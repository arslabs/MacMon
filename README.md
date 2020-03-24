# MacMon

![MacMon](/imgs/MacMon.jpg)

Display CPU temperature &amp; FAN RPM

1. Connect Feather M0 or arduino nano to the mac
2. Execute 'find_serial.py' for getting pid, vid, serial number for serial port
```
Macmini:macmon $ ./find_serial.py
/dev/cu.Bluetooth-Incoming-Port - n/a, vid: None, pid: None, serial no.: None
/dev/cu.usbmodem1463201 - Feather M0, vid: 9114, pid: 32779, serial no.: 25657693514D503259202020FF101F3E
```
3. Change 'config.json' appropriately. MacMon use serial_no first for finding the device. Otherwise use vid & pid for finding the device.
```
Macmini:macmon $ cat config.json
{
	"baud":115200,
	"duration": 2,
	"vid":9114,
	"pid":32779,
	"serial_no":"25657693514D503259202020FF101F3E"
}
```
4. Execute 'macmon.py' with root privilidge for opening serial port
```
Macmini:macmon $ nohup ./macmon.py &
```

* Hardware connections can be found in Hardware directory.
* Arduino sketch (/Arduino/MacTempFan.ino) can be used for Adafruit Feather M0 and Arduino Nano without any modification.
