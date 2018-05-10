import requests
import json
import datetime

from obd_utils import *
from obd_io import *

logger = Logger()
system_active = True

class HeadlessReporter(object):

  def __init__(self, root_url, device_email, device_password, delay=3):
    """
    This class will handle gathering sensor data from the vehicle
    and post this data to the specified url

    :param root_url: The root url of the api to be used
    :param device_email: The email of the current device
    :param device_password: The password for the current device
    :param delay: How often the device should publish data
    """
    self.port = None
    self.sensor_list = []
    self.root_url = root_url
    self.email = device_email
    self.password = device_password
    self.device_name = ""
    self.headers = {'Content-Type': 'application/json'}
    self.delay = delay

  def connect(self):
    """
    Connect to the OBD reader
    """
    portnames = scan_serial()
    logger.log(portnames)
    for port in portnames:
      self.port = OBDPort(port, None, 2, 2)
      if self.port.State == 0:
        self.port.close()
        self.port = None
      else:
        break

    if self.port:
      logger.log("Connected to " + self.port.port.name)

  def is_connected(self):
    return self.port

  def device_login(self):
    """
    Requests an authentication token from the api and sets a reusable headers attribute
    """
    payload = {'email': self.email, 'password': self.password}
    r = requests.post("%sv1/device_sessions" % self.root_url, data=payload)
    content = json.loads(r.content)
    self.device_name = content['device_name']
    self.headers['X-Device-Email'] = self.email
    self.headers['X-Device-Token'] = content['authentication_token']

  def device_logout(self):
    """
    Logs out the device, resetting the authentication token
    """
    r = requests.delete("%sv1/device_sessions" % self.root_url, headers=self.headers)
    if r.status_code == 200:
      logger.log("Successfully logged out")
    else:
      logger.log("Problem logging out")

  def get_requested_sensors(self):
    """
    Requests all of the sensors requested by the owner of the device
    :return: The list of requested sensors
    """
    r = requests.get("%sv1/sensors" % self.root_url, headers=self.headers)
    return json.loads(r.content)

  def create_report(self):
    """
    Generates a report with a timestamp, device name, and a list of sensor readings
    :return: The created report
    """
    report = {"time_reported": str(datetime.datetime.now()), "device_name": self.device_name, "readings": []}
    for sensor in self.sensor_list:
      value = self.get_data_for_sensor(sensor)
      if value is not None:
        report['readings'].append({"shortname": sensor["shortname"], "value": str(value)})
    return report

  def publish_report(self, report):
    """
    Publishes a report to the web service
    :param report: The report to be published
    """
    r = requests.post("%sv1/reports" % self.root_url, headers=self.headers, data=json.dumps(report))
    logger.log(r.content)

  def get_data_for_sensor(self, requested_sensor):
    """
    Retrieves the value for the specified sensor
    :param requested_sensor: The requested sensor
    :return: The current measured value for that sensor, or None if there was an issue
    """
    if self.port is None:
      return None
    for index, sensor in enumerate(obd_sensors.SENSORS):
      if sensor.shortname == requested_sensor["shortname"]:
        try:
          (name, value, unit) = self.port.sensor(index)
          return value
        except InvalidResponseCode:
          logger.log("Invalid response code returned\n\tsensor:\t%s\n" % sensor.shortname)
          return None

  def run(self):
    self.device_login()
    while not self.is_connected():
      self.connect()
    while system_active:
      self.sensor_list = self.get_requested_sensors()
      report = self.create_report()
      self.publish_report(report)
      x = 0
      while x <= 100 and system_active:
        time.sleep(self.delay/100)
        x += 1
    self.device_logout()
