import requests
import json
import time

from obd_utils import Logger
from datetime import datetime
from obd_data_generator import ObdDataGenerator

logger = Logger()
system_active = True

class DummyHeadless(object):

  def __init__(self, root_url, device_email, device_password, delay=10):
    """
    This class will act as a dummy reporter for OBD data for the purpose of
    showcasing the project where I will not have access to a car with an
    OBD port. It will behave in the exact same way that the regular headless
    reported will but will generate fake data instead of accessing the OBD.

    :param root_url: The root url of the api to be used
    :param device_email: The email of the current device
    :param device_password: The password for the current device
    :param delay: How often the device should publish data
    """
    self.sensor_list = []
    self.root_url = root_url
    self.email = device_email
    self.password = device_password
    self.device_name = ""
    self.headers = {'Content-Type': 'application/json'}
    self.delay = delay
    self.generator = ObdDataGenerator()

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
    report = {"time_reported": str(datetime.now()), "device_name": self.device_name, "readings": []}
    for sensor in self.sensor_list:
      value = self.get_data_for_sensor(sensor)
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
    Generates a value for the specified sensor
    :param requested_sensor: The requested sensor
    :return: The generated value for that sensor
    """
    return self.generator.generate(requested_sensor["shortname"])

  def run(self):
    self.device_login()
    while system_active:
      self.sensor_list = self.get_requested_sensors()
      report = self.create_report()
      self.publish_report(report)
      x = 0
      while x <= 100 and system_active:
        time.sleep(self.delay/100)
        x += 1
    self.device_logout()
