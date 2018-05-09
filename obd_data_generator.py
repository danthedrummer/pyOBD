import random
import datetime
from obd_utils import Logger

logger = Logger()

class ObdDataGenerator(object):
  """
  This class generates fake data to represent information gathered from an OBD port
  """

  def generate(self, sensor_name):
    """
    Attempts to generate fake data for the specified sensor

    :param sensor_name: the sensor to have data generated
    :return: The random value generated
    :raises: AttributeError if the sensor is not supported
    """
    logger.log("generating %s" % sensor_name)
    return getattr(self, sensor_name)()

  def temp(self):
    """
    Generates coolant temperature data. Safe limits are between 0 and 130 degrees Celcius

    :return: The randomly generated value
    """
    try:
      coolant_temp = self.coolant_temp
    except AttributeError:
      coolant_temp = random.randint(15, 30)

    if coolant_temp > 100 and random.uniform(0, 1) > 0.8:
      coolant_temp = random.randint(-5, 30)
    else:
      coolant_temp += random.randint(-2, 10)
    self.coolant_temp = coolant_temp
    return coolant_temp

  def rpm(self):
    """
    Generates engine RPM data. Has an upper safe limit of 9000

    :return: The randomly generated value
    """
    try:
      rpm_data = self.rpm_data
      rpm_up = self.rpm_up
    except AttributeError:
      rpm_data = random.randint(0, 4000)
      rpm_up = True

    if rpm_up and rpm_data < 7000:
      rpm_data += random.randint(50, 300)
    elif not rpm_up and rpm_data > 500:
      rpm_data -= random.randint(50, 300)

    if rpm_data > 7000:
      rpm_up = False
    elif rpm_data < 500:
      rpm_up = True
      if rpm_data < 0:
        rpm_data = 0

    self.rpm_up = rpm_up
    self.rpm_data = rpm_data
    return rpm_data


  def speed(self):
    """
    Generates vehicle speed data. Has no limits but should be reasonable

    :return: The randomly generated value
    """
    try:
      speed_data = self.speed_data
      speed_up = self.speed_up
    except AttributeError:
      speed_data = random.randint(0, 60)
      speed_up = True

    if speed_up and speed_data < 100:
      speed_data += random.randint(2, 10)
    elif not speed_up and speed_data > 0:
      speed_data -= random.randint(2, 10)
      if speed_data < 0:
        speed_data = 0

    if speed_data > 100:
      speed_up = False
    elif speed_data == 0:
      speed_up = True

    self.speed_up = speed_up
    self.speed_data = speed_data
    return speed_data

  def intake_air_temp(self):
    """
    Generates intake air temp data. Safe ranges between -5 and 25 degrees Celsius

    :return: The randomly generated value
    """
    return random.randint(-7, 30)

  def maf(self):
    """
    Generates air flow rate data. Has a lower limit of 0

    :return: The randomly generated value
    """
    try:
      flow_rate = self.flow_rate
    except AttributeError:
      self.flow_rate = random.randint(1000, 1500)
      flow_rate = self.flow_rate

    flow_rate = flow_rate - random.randint(-100, 100)

    return flow_rate

  def fuel_level(self):
    """
    Generates fuel level data. Percentage value

    :return: The randomly generated value
    """
    try:
      fuel_level = self.fuel_level_data
    except AttributeError:
      fuel_level = random.randint(45, 70)

    if fuel_level < 15:
      fuel_level = random.randint(45, 70)
    else:
      fuel_level += random.randint(-5, -2)
    self.fuel_level_data = fuel_level
    return fuel_level

  def control_module_voltage(self):
    """
    Generates battery voltage level data. Safe limit between 14.7 and 12.4 Volts

    :return: The randomly generated value
    """
    try:
      battery_voltage = self.battery_voltage
    except AttributeError:
      battery_voltage = random.uniform(12.7, 14.3)

    battery_voltage += random.uniform(-(battery_voltage - 12.0), (15.0-battery_voltage))
    self.battery_voltage = battery_voltage
    return battery_voltage

  def ambient_air_temp(self):
    """
    Generates ambient air temperature data. Has no limits but should be reasonable

    :return: The randomly generated value
    """
    ambient_temp = random.randint(10, 15) + random.uniform(-0.5, 0.5)
    return ambient_temp

  def oil_temp(self):
    """
    Generates engine oil temperature data. Safe limits between 30 and 130 degrees Celsius
    :return:
    """
    try:
      oil_temp_data = self.oil_temp_data
    except AttributeError:
      oil_temp_data = random.randint(30, 40)

    if oil_temp_data > 100 and random.uniform(0, 1) > 0.8:
      oil_temp_data = random.randint(28, 40)
    else:
      oil_temp_data += random.randint(-2, 10)
    self.oil_temp_data = oil_temp_data
    return oil_temp_data
