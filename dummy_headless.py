import sys
import obd_sensors
import requests
import json
import time

from obd_utils import Logger
from datetime import datetime

logger = Logger()
system_active = True

class DummyHeadless(object):
  """
  This class will act as a dummy reporter for OBD data for the purpose of
  showcasing the project where I will not have access to a car with an
  OBD port. It will behave in the exact same way that the regular headless
  reported will but will generate fake data instead of accessing the OBD.
  """
  def __init__(self, root_url, device_email, device_password, additional_params=None):
    self.sensor_list = []
    self.root_url = root_url
    self.email = device_email
    self.password = device_password
    self.headers = {}
    if additional_params is None or type(additional_params) != dict:
      self.additional_params = {}
    else:
      self.additional_params = additional_params

  def device_login(self):
    payload = {'email': self.email, 'password': self.password}
    r = requests.post("%sv1/device_sessions" % self.root_url, data=payload)
    content = json.loads(r.content)
    print(content)
    self.headers['X-Device-Email'] = self.email
    self.headers['X-Device-Token'] = content['authentication_token']
    self.get_requested_sensors()

  def get_requested_sensors(self):
    r = requests.get("%sv1/sensors" % self.root_url, headers=self.headers)
    print(r.status_code)
    self.sensor_list = json.loads(r.content)
    print(self.sensor_list)

  def run(self):
    self.device_login()
    while system_active:
      ...


try:
  with open('headless_device_config', 'r') as config_file:
    url = config_file.readline().strip()
    email = config_file.readline().strip()
    password = config_file.readline().strip()
  reporter = DummyHeadless(url, email, password)
  reporter.run()
  while True:
    pass
except KeyboardInterrupt:
  logger.log("Shutting down...")
finally:
  system_active = False
  sys.exit(0)


