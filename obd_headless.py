# Entry point for using the pyOBD tool headless
# Based on obd_recorder from https://github.com/Pbartek/pyobd-pi/

import obd_io
import obd_sensors
import serial
import requests
import json

from obd_utils import scan_serial
from datetime import datetime


"""
This class will handle gathering sensor data from the vehicle
and post this data to the specified url 
"""
class headless_reporter():
    def __init__(self, url, requested_sensors):
        self.port = None
        self.sensor_list = []
        self.url = url
        
        for sensor in requested_sensors:
            if sensor != "unknown":
                self.add_sensor(sensor)
        
    def connect(self):
        portnames = scan_serial() #TODO: Add in the obd_utils 
        print(portnames) #TODO: Remove. Just here for debug
        for port in portnames:
            self.port = obd_io.OBDPort(port, None, 2, 2)
            if(self.port.State == 0):
                self.port.close()
                self.port = None
            else:
                break
            
        if (self.port):
            print("Connected to " + self.port.port.name)
            
    def is_connected(self):
        return self.port
        
    def add_sensor(self, sensor):
        for index, e in enumerate(obd_sensors.SENSORS):
            if (sensor == e.shortname):
                self.sensor_list.append(sensor)
                print("Reporting sensor: " + e.name)
                break
            
    def gather_data(self):
        if (self.port is None):
            return None
            
        print("Gathering sensor data")
        
        while(True):
            readings = {}
            readings["time"] = datetime.now()
            
            for sensor in self.sensor_list:
                (name, value, unit) = self.port.sensor(sensor)
                readings[obd_sensors.SENSORS[sensor].shortname] = value
                
            self.publish_data(readings)
            
    def publish_data(self, readings):
        r = requests.post(self.url, data=readings)
        print("Content ~> " + str(json.loads(r.content)))
        print("Status ~> " + str(r.status_code))
        
requested_sensors = ["rpm", "speed", "throttle_pos", "load", "fuel_status"]
reporter = headless_reporter("https://vehilytics-proto-v2.herokuapp.com/readings", requested_sensors)
reporter.connect()

if not reporter.is_connected():
    print("Not connected")
reporter.gather_data()
