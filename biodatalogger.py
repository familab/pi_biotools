#!/usr/bin/python2.7
"""
Biodatalogger
2015-08-15
"""

import urllib2
import time
import ConfigParser
import traceback
import os.path
from datetime import datetime

# External (please pip install as needed)
import daemon
from w1thermsensor import W1ThermSensor

# Read globals
CONFIG_FILE = 'biodatalogger.ini'
CONFIG = ConfigParser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE))

CSV_FILEPATH = CONFIG.get('global', 'csv_filepath')
THINGSPEAK = CONFIG.get('global', 'thingspeak')
WAIT_TIME_SECONDS = CONFIG.getint('global', 'wait_time_seconds')

class Collector(object):
    def __init__(self):
        self.sensor = W1ThermSensor()

    def save_csv(self, data):
        filepath = CSV_FILEPATH.format(datetime.now().strftime("%Y-%m-%d"))
        with open(filepath, "a") as fh:
            fh.write("{0},{1},{2},{3},{4}\n".format(*data))

    def save_thingspeak(self, data):
        try:
            url = THINGSPEAK.format(data[1], data[2], data[3], data[4])
            urllib2.urlopen(url)
        except:
            print traceback.print_exc()
            print "Still going...."

    def save_console(self, data):
       # print "{0} Current temp_c: {1}, temp_f: {2}".format(*data)
        print "{0} Current temp_c: {1}, temp_f: {2}, album {3}, image {4}".format(*data)
    def collect_forever(self):
        while True:
            now = datetime.now()
            temp_c, temp_f = self.sensor.get_temperatures([W1ThermSensor.DEGREES_C, W1ThermSensor.DEGREES_F])
            data = [now, temp_c, temp_f]
            self.save_console(data)
            self.save_csv(data)
            self.save_thingspeak(data)
            time.sleep(WAIT_TIME_SECONDS)
            

if __name__ == "__main__":
#    with daemon.DaemonContext():
        collector = Collector()
        collector.collect_forever()

