"""Main module."""

import json
import os
import sys
from datetime import datetime
from file_read_backwards import FileReadBackwards
sys.path.append("../")
from moisture_sensor.moisture_sensor import MoistureSensor
from light_sensor.light_sensor import light_sensor
from gps.gps import GPS
###########################################################################3#

###############################################################################
class AgroKit:
    '''AgroKit class to interface with hardware'''

    def __init__(self):
        """ Instantiate AgroKit object with default values and other sensor attributes """
        self.MS = MoistureSensor(21, 0, 7, 18)
        self.GPS = GPS()
        self.LS = light_sensor(17, 17)
        #defaults:
        MAX_MOISTURE = 100
        MIN_MOISTURE = 0
        MAX_LUX = 500
        MIN_LUX = 0


    def read(self):
        """ Method to read and return moisture, light and GPS data from sensors as a Reading object """
        #loc = self.GPS.getLongLat()
        loc = self.GPS.getLongLat(self.GPS.getGLL())
        RMC_msg = self.GPS.getRMC()
        GGA_msg = self.GPS.getGGA()
        alt = GGA_msg.altitude
        dt = RMC_msg.datetime #time stamp
        str_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
        moisture = round(self.MS.singleRead()) #moisture level as a percentage
        try:
            light = self.LS.singleReadLux()
        except Exception as e:
            print(e)
            light = 100
            self.LS.powerDown(17)
        output = str_datetime + "\tMoisture: " + str(moisture) + "\tLux: " + str(light) + "\tLocation:" + loc + "\tAltitude: " + str(alt) +"\n"
        print(output)
        return Reading(moisture,light, RMC_msg)



    def loadProfile(self,name):
        """ Method to load values from stored profile into AgroKit object variables

        arguments:
        name -- name of profile to load
        """
        with open("profiles.json", 'r') as f:
            try:
                profile = json.load(f)
                self.MAX_MOISTURE = profile[name]["moisture"][1]
                self.MIN_MOISTURE = profile[name]["moisture"][0]
                self.MAX_LUX = profile[name]["lux"][1]
                self.MIN_LUX = profile[name]["lux"][0]
                print("Profile " + '\'' + name + "\' loaded.\n")
            except Exception as e:
                print(e)
                print('Profile does not exist')

    def readingOK(self,reading, msg):
        """ Check if reading values fall within the ranges loaded from active profile and return a boolean

        arguements:
        reading -- Reading object
        msg -- string thats passed into method which is changed to give more info about the current reading
        """
        ok = True
        if reading.moisture < self.MIN_MOISTURE or reading.moisture > self.MAX_MOISTURE or reading.lux < self.MIN_LUX or reading.lux > self.MAX_LUX:
            ok = False
            if reading.moisture < self.MIN_MOISTURE:
                msg[0] = "Moisture too low;"
            elif reading.moisture > self.MAX_MOISTURE:
                msg[0] = "Moisture too high;"
            if reading.lux < self.MIN_LUX:
                msg[0] = msg[0] + "lux too low\n"
            elif  reading.lux > self.MAX_LUX:
                msg[0] = msg[0] + "lux too high\n"
        else:
            msg[0] = 'Moisture and lux within range of current profile'
        return ok


    def logData(self, rmc, gga, gll, moist, lux, filename):
        """ Method to write information to a text file

        arguments:
        rmc -- pymnea2 nmea object for GPRMC message
        gga -- pymnea2 nmea object for GPGGA message
        gll -- pymnea2 nmea object for GPGLL message
        moist -- moisture reading as a number
        lux -- lux reading as a number
        filename -- name of log file
        """
        dt = rmc.datetime #time stamp
        time = dt.strftime("%Y-%m-%d %H:%M:%S")
        alt = gga.altitude
        loc = self.GPS.getLongLat(gll)
        string = time + "\t" + str(moist) + "\t" + str(lux) + "\t" + str(alt) + "\t\t" + loc + '\n'
        print(string)

        if os.path.exists(filename):
            with open('log.txt', 'a') as f:
                f.write(string)
                f.close()
        else:
            with open(filename, 'a') as f:
                f.write("Time\t\t\tMoisture\t\tLux\t\t\tAltitude\t\tLocation\n")
                f.write(string)
                f.close()

    def last24Hrs(self, filename):
        """ Method to display data logged within past 24 hours to a text file

        arguments:
        filename -- name of log text file
        """
        try:
            now = datetime.utcnow()
            print("Time\t\t\tMoisture\t\tLux\t\t\tAltitude\t\tLocation\n")
            with FileReadBackwards('log.txt', encoding="utf-8") as f:
                for line in f:
                    try:
                        date = datetime.strptime(line[0:19], "%Y-%m-%d %H:%M:%S")
                    except:
                        break #if can't then we've reached the top line so break
                    if (now - date).days == 0: #within 24 hours
                        print(line)
                    else:
                        break
        except Exception as e:
            print(e)


    @classmethod
    def createProfile(cls, name, minMoisture, maxMoisture, minLux, maxLux):
        """ Method to create a custom sensor profile with moisture and lux ranges

        arguments:
        name -- name of new profile
        minMoisture -- minimum value for moisture
        maxMoisture -- maximum value for moisture
        minLux -- minimum value for lux
        maxLux -- maximum value for lux
        """
        entry = { name: {"moisture": [minMoisture, maxMoisture], "lux": [minLux, maxLux]}}
        with open("profiles.json", "r") as f:
            try:
                profile = json.load(f)
            except:
                profile = {}
        with open("profiles.json", "w") as h:
            profile.update(entry)
            try:
                json.dump(profile,h, indent = 4)
            except Exception as e:
                print(e)

#############################################################################
#class for agro_kit reading:
#############################################################################

class Reading:
    """ Class to represent an aggregate reading from moisture sensor, light sensor and GPS """
    def __init__(self, moisture, lux, gps):
        """ Instantiate Reading object from keyword arguments

        arguments:
        moisture -- moisture reading as number
        lux -- lux reading as number
        gps -- pynmea2 nmea GPRMC object
        """
        self.moisture = moisture
        self.lux = lux
        self.gps = gps
#############################################################################



if __name__ == "__main__":
    myAG = AgroKit()
    myAG.loadProfile("test")
    myAG.LS.singleReadLux()
