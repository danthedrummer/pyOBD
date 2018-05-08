import random
from obd_utils import Logger

logger = Logger()

class ObdDataGenerator(object):

  def generate(self, sensor_name):
    try:
      getattr(self, sensor_name)()
    except AttributeError:
      logger.log("No generator for %s" % sensor_name)

  def temp(self):
    logger.log("generating temp")
    ...

  def rpm(self):
    logger.log("generating rpm")
    ...

  def speed(self):
    logger.log("generating speed")
    ...

  def intake_air_temp(self):
    logger.log("generating intake air temp")
    ...

  def maf(self):
    logger.log("generating maf")
    ...

  def fuel_level(self):
    logger.log("generating fuel level")
    ...

  def control_module_voltage(self):
    logger.log("generating control module voltage")
    ...

  def ambient_air_temp(self):
    logger.log("generating ambient air temp")
    ...

  def oil_temp(self):
    logger.log("generating oil temp")
    ...
