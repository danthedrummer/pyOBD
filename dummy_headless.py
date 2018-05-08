import sys
import obd_sensors
import requests
import json
import time

from obd_utils import Logger
from datetime import datetime
from obd_data_generator import ObdDataGenerator
from threading import Thread

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
    self.device_name = ""
    self.headers = {'Content-Type': 'application/json'}
    if additional_params is None or type(additional_params) != dict:
      self.additional_params = {}
    else:
      self.additional_params = additional_params

  def device_login(self):
    payload = {'email': self.email, 'password': self.password}
    r = requests.post("%sv1/device_sessions" % self.root_url, data=payload)
    content = json.loads(r.content)
    self.device_name = content['device_name']
    self.headers['X-Device-Email'] = self.email
    self.headers['X-Device-Token'] = content['authentication_token']

  def get_requested_sensors(self):
    r = requests.get("%sv1/sensors" % self.root_url, headers=self.headers)
    self.sensor_list = json.loads(r.content)

  def run(self):
    self.device_login()
    generator = ObdDataGenerator()
    while system_active:
      self.get_requested_sensors()
      report = {"time_reported": str(datetime.now()), "device_name": self.device_name, "readings": []}
      for sensor in self.sensor_list:
        value = generator.generate(sensor['shortname'])
        report['readings'].append({"shortname": sensor["shortname"], "value": str(value)})
      r = requests.post("%sv1/reports" % self.root_url, headers=self.headers, data=json.dumps(report))
      print(r.content)
      time.sleep(10)


try:
  with open('headless_device_config', 'r') as config_file:
    url = config_file.readline().strip()
    email = config_file.readline().strip()
    password = config_file.readline().strip()
  reporter = DummyHeadless(url, email, password)
  Thread(target=reporter.run).start()
  while system_active:
    pass
except KeyboardInterrupt:
  print("Shutting down...")
finally:
  system_active = False
  sys.exit(0)


