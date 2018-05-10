import unittest
from obd_data_generator import ObdDataGenerator

class ObdDataGeneratorTests(unittest.TestCase):

  def setUp(self):
    self.generator = ObdDataGenerator()

  def tearDown(self):
    self.generator = None

  def testCallingGenerateWithASupportedSensorNameShouldReturnANumber(self):
    value = self.generator.generate("temp")
    self.assertTrue(type(value) in [int, float])

  def testCallingGenerateWithAnUnsupportedSensorNameShouldRaiseAttributeError(self):
    with self.assertRaises(AttributeError):
      self.generator.generate("wubalub")

  # Testing Temp Generator
  def testGeneratingTempValuesShouldNeverReturnBelowNegative10(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("temp") > -10)

  def testGeneratingTempValuesShouldNeverReturnNoneValue(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("temp") is not None)

  # Testing RPM generator
  def testGenerateRpmShouldNeverReturnLessThanZero(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("rpm") >= 0)

  def testGenerateRpmShouldNeverReturnNoneValue(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("rpm") is not None)

  def testGenerateRpmShouldNeverReturnAbove9000(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("rpm") < 9000)

  # Testing speed generator
  def testGenerateSpeedShouldNeverReturnLessThanZero(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("speed") >= 0)

  def testGenerateSpeedShouldNeverReturnNoneValue(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("speed") >= 0)

  def testGenerateSpeedShouldNeverReturnAbove130(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("speed") < 130)

  # Testing IntakeAirTemp generator
  def testGenerateIntakeAirTempShouldNeverReturnLessThanNegative10(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("intake_air_temp") >= -10)

  def testGenerateIntakeAirTempShouldNeverReturnNoneValue(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("intake_air_temp") is not None)

  def testGenerateIntakeAirTempShouldNeverReturnAbove30(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("intake_air_temp") <= 30)

  # Testing air flow rate generator
  def testGenerateMafShouldNeverReturnLessThan900(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("maf") >= 900)

  def testGenerateMafShouldNeverReturnNoneValue(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("maf") is not None)

  def testGenerateMafShouldNeverReturnAbove1600(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("maf") <= 1600)

  # Testing fuel level generator
  def testGenerateFuelLevelShouldNeverReturnBelow0(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("fuel_level") >= 0)

  def testGenerateFuelLevelShouldNeverReturnNoneValue(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("fuel_level") is not None)

  def testGenerateFuelLevelShouldNeverReturnAbove100(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("fuel_level") <= 100)

  # Testing control module voltage generator
  def testGenerateBatteryVoltageShouldNeverReturnBelow12(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("control_module_voltage") >= 12.0)

  def testGenerateBatteryVoltageShouldNeverReturnNoneValue(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("control_module_voltage") is not None)

  def testGenerateBatteryVoltageShouldNeverReturnAbove15(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("control_module_voltage") <= 15.0)

  # Testing ambient air temp
  def testGenerateAmbientAirTempShouldNeverReturnLessThan8(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("ambient_air_temp") >= 8.0)

  def testGenerateAmbientAirTempShouldNeverReturnNoneValue(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("ambient_air_temp") is not None)

  def testGenerateAmbientAirTempShouldNeverReturnAbove18(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("ambient_air_temp") <= 17.0)

  # Testing oil temp
  def testGenerateOilTempShouldNeverReturnLessThan10(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("oil_temp") >= 10)

  def testGenerateOilTempShouldNeverReturnNoneValue(self):
    for x in range(0, 100):
      self.assertTrue(self.generator.generate("oil_temp") is not None)

