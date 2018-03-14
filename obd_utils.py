import serial
import platform

"""
Scan for all available ports

@return: The list of available ports
"""
def scan_serial():
    available_ports = []
    
    #Bluetooth
    for i in range(10):
        try:
            s = serial.Serial("/dev/rfcomm"+str(i))
            available_ports.append(str(s.port))
            s.close()
        except serial.SerialException:
            pass
        
    #USB
    for i in range(256):
        try:
            s = serial.Serial("/dev/ttyUSB"+str(i))
            available_ports.append(s.portstr)
            s.close()
        except serial.SerialException:
            pass
        
    return available_ports