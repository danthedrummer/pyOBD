import serial
import platform
import sys

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

class Logger(object):

  class __Logger(object):

    def __init__(self):
      try:
        if "--debug" in sys.argv:
          self.enabled = True
      except IndexError:
        self.enabled = False

    def __log(self, message):
      if self.enabled:
        print(message)

  instance = None

  def __init__(self):
    if not Logger.instance:
      Logger.instance = Logger.__Logger()

  def log(self, message):
    self.instance.__log(message)