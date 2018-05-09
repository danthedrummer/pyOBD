Vehilytics OBD Reporter
=====

## Description
This system forms a part of my final year project and is coded to work specifically with
my own API, so may not be appropriate for general use.

### pyOBD_headless
Building on to the pyOBD tool to allow it to be used headless.

Fork from https://github.com/chethenry/pyOBD, which is a fork from http://www.obdtester.com/pyobd.

### Requirements
An ELM 32x OBD-II interface
Python 2.x or greater
pySerial
A car supporting OBD-II

### Additions In This Fork
* Program can operate headless
* Sensor readings can be published to a url to allow an API to process or persist the data remotely


