# Entry point for using the pyOBD tool headless
# Based on obd_recorder from https://github.com/Pbartek/pyobd-pi/

import obd_sensors
import serial
import requests
import json
import time

from obd_utils import *
# Passing --debug as a command line argument will
# enable print statements otherwise they are ignored
logger = Logger()

from obd_io import *
from datetime import datetime

class headless_reporter():
  """
  This class will handle gathering sensor data from the vehicle
  and post this data to the specified url

  @param requested_sensors: a list of sensors to be polled
  @param url: the url to receive the data
  @param additional_params: a dictionary of extra parameters that may be required
  """
  def __init__(self, requested_sensors, url, additional_params={}):
    self.port = None
    self.sensor_list = []
    self.url = url
    self.additional_params = additional_params

    for sensor in requested_sensors:
      if sensor != "unknown": # The default shortname for a sensor is "unknown" so it should be ignored
        self.add_sensor(sensor)

  def connect(self):
    portnames = scan_serial()
    logger.log(portnames)
    for port in portnames:
      self.port = obd_io.OBDPort(port, None, 2, 2)
      if(self.port.State == 0):
        self.port.close()
        self.port = None
      else:
        break

    if (self.port):
      logger.log("Connected to " + self.port.port.name)

  def is_connected(self):
    return self.port

  def add_sensor(self, sensor):
    for index, e in enumerate(obd_sensors.SENSORS):
      if (sensor == e.shortname):
        self.sensor_list.append(sensor)
        logger.log("Reporting sensor: " + e.name)
        break

  def gather_data(self):
    if (self.port is None):
      return None

    logger.log("Gathering sensor data")

    while(True):
      readings = {}
      readings["readings_taken_at"] = datetime.now()

      for index, sensor in enumerate(obd_sensors.SENSORS):
        if sensor.shortname in self.sensor_list:
          try:
            (name, value, unit) = self.port.sensor(index)
          except InvalidResponseCode:
            logger.log("Invalid response code returned\n\tsensor:\t%s\n" % (sensor.shortname))
            value = "invalid"
          readings[sensor.shortname] = value

      self.publish_data(readings)
      time.sleep(5)

  def publish_data(self, readings):
    # I'm disabling the post requests until I have an endpoint to use
    data = self.additional_params
    for key in readings:
      data[key] = readings[key]

    logger.log("Publishing Data")
    logger.log("Url ~> " + str(self.url))
    logger.log("Readings ~> " + str(data))

    # TODO: Remove this file writing section
    # Writing the collected data to a file for my own record
    with open("recorded_obd_data", 'a') as file:
      file.write(json.dumps(data, default=str) + "\n")

    #TODO: re-enable this code
    # r = requests.post(self.url, data=readings)
    # logger.log("Content ~> " + str(json.loads(r.content)))
    # logger.log("Status ~> " + str(r.status_code))

requested_sensors = [
  "fuel_level",
  "control_module_voltage",
  "ambient_air_temp"
]
reporter = headless_reporter(requested_sensors,"https://vehilytics-proto-v2.herokuapp.com/readings")
reporter.connect()

if not reporter.is_connected():
  logger.log("Not connected")
reporter.gather_data()
