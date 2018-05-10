# Entry point for using the pyOBD tool headless
# Based on obd_recorder from https://github.com/Pbartek/pyobd-pi/

from threading import Thread
from obd_utils import Logger

# Passing --debug as a command line argument will
# enable print statements otherwise they are ignored
logger = Logger()
system_active = True

try:
  with open('headless_device_config', 'r') as config_file:
    url = config_file.readline().strip()
    email = config_file.readline().strip()
    password = config_file.readline().strip()
    if config_file.readline().strip() == "dummy":
      from dummy_headless import *
      reporter = DummyHeadless(url, email, password)
    else:
      from headless_reporter import *
      reporter = HeadlessReporter(url, email, password)
  Thread(target=reporter.run).start()
  while system_active:
    pass
except KeyboardInterrupt:
  logger.log("Shutting down...")
finally:
  logger.log("Cleaning up...")
  system_active = False
  sys.exit(0)
