import unittest

from dummy_headless import DummyHeadless

class DummyReporterTests(unittest.TestCase):

  def setUp(self):
    self.reporter = DummyHeadless("https://vehilytics-api.herokuapp.com/", "tests@example.com", "password")

  def tearDown(self):
    self.reporter = None

  def testCreateReportShouldCreateAReportDictionary(self):
    report = self.reporter.create_report()
    self.assertTrue("time_reported" in report.keys())

  def testCreateReportShouldNeverReturnNone(self):
    report = self.reporter.create_report()
    self.assertTrue(report is not None)

  def testGetDataForSensorShouldNotReturnNoneForValidSensor(self):
    value = self.reporter.get_data_for_sensor({"shortname": "temp"})
    self.assertTrue(value is not None)

  def testGetDataForSensorShouldRaiseAttributeErrorForInvalidSensor(self):
    with self.assertRaises(AttributeError):
      self.reporter.get_data_for_sensor({"shortname": "wubalub"})

