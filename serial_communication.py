from serial.tools import list_ports
import serial

COMPORT = ''

def available_ports(port):
	global COMPORT
	for i in list_ports.comports():
		if port == i.device:
			COMPORT = serial.Serial(port, timeout=1)
			return True
	return False