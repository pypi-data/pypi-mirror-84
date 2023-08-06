""" GPS Library """

import json
import serial
from time import sleep
from time import time
import pynmea2 as nmea
import requests
import sys

class GPS():
    """ Class to represent a GPS sensor object """

    """Attributes:
    BAUD_RATES -- list of supported baud rates for GPS Sensor
    BAUD_RATE_CHKSUMS -- dictionary of NMEA check sums for the manufacturer NMEA commands to configure baud rate of GPS Sensor
    PQEPE_CHKSUMS -- dictionary of NMEA checksums for manufacturer commands to configure URC messages for GPS Sensor
    PQFLP -- dictionary of NMEA checksums for manufacturer commands to configure low power mode for GPS Sensor
    API_KEY -- user's Google API key if they want Distance Matric functionality (default "")
    """

    BAUD_RATES = [4800, 9600, 14400, 19200, 38400, 57600, 115200]
    BAUD_RATE_CHKSUMS = {'4800': "48", '9600': '4B', '14400': '75', '19200': '7E', '38400': '7B', '57600': '70', '115200': '43'}
    PQEPE_CHKSUMS = {'0,0': '2A', '0,1': '2B', '1,0': "2B", '1,1': '2A' }
    PQFLP_CHKSUMS = {'0,0': '20', '0,1': '21', '1,0': '21', '1,1': '20'}

    #Static Var
    #ser = serial.Serial ("/dev/ttyS0", 9600 , timeout=1)
    API_KEY = '' # empty by default


    def __init__(self, baud_rate = 9600, timeout = 5):
        """ Instantiate object of GPS class using keyword arguments

        arguments:
        baud_rate -- baud rate of serial port on Raspberry Pi (default 9600)
        timeout -- delay before timing out when reading from serial port  (default 5 seconds)
        """

        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = serial.Serial ("/dev/ttyS0", self.baud_rate, self.timeout)
        self.ser.baudrate = baud_rate
        self.ser.timeout = timeout


#######################################################################################3ss
#Configuration methods
#######################################################################################3



    def setGPSBaudRate(self, baud_rate):    #note that only baud rates of 4800, 9600, 14400, 19200, 38400, 57600, 115200 are allowed
        """ Method to configure the baud rate of the GPS module

        arguments:
        baud_rate -- baud rate of GPS module
        """
        if baud_rate in GPS.BAUD_RATES:
            str_baud_rate = str(baud_rate)
            cmd = '$PQBAUD,W,' + str_baud_rate + '*' + GPS.BAUD_RATE_CHKSUMS[str_baud_rate] + "\r\n"
            self.ser.write(cmd.encode())
            sleep(0.1)
            self.ser.baudate = baud_rate # set /dev/ttyS0 baudrate as well
            sleep(1.2)
            response = self.ser.readline().decode()
            print(response)
        else:
            print("Error - invalid baud rate. Can only choose from 4800, 9600, 14400, 19200, 38400, 57600, 115200.")

    def enableURC(self, mode, save):
        """ Method to enable GPS to read PQEPE NMEA messages

            arguments:
            mode -- 1 to enable, 0 to disable
            save -- 1 to save new setting, 0 to keep setting only for current power cycle
            """
        str_mode, str_save, = '0','0'   #declaring vars
        if mode:
            str_mode = "1"
        if save:
            str_save = '1'
        arg = str_mode + "," + str_save
        cmd = "$PQEPE,W," + arg + "*" + GPS.PQEPE_CHKSUMS[arg] + "\r\n"
        self.ser.write(cmd.encode())
        #response = self.getPQEPE()
        #print(response)


    def enableFLP(self,mode, save ):
        """ Method to enable Low Power Mode on the GPS module

        arguments:
        mode -- 1 to enable, 0 to disable
        save -- 1 to save new setting, 0 to keep setting only for current power cycle
        """
        str_mode, str_save, = '0','0' #declaring vars
        if mode:
            str_mode = "1"
        if save:
            str_save = '1'
        arg = str_mode + "," + str_save
        cmd = "$PQFLP,W," + arg + "*" + GPS.PQFLP_CHKSUMS[arg] + "\r\n"
        self.ser.write(cmd.encode())

    def coldstart(self):
        """ Restart the GPS module removing most cached satellite data """
        self.ser.write("$PMTK103*30\r\n".encode())

    def fullColdStart(self):
        """ Restart the GPS module removing all cached satellite data """
        self.ser.write("$PMTK104*37\r\n".encode())

    def warmStart(self):
        """ Restart the GPS module removing some cached satellite data """
        self.ser.write("$PMTK102*31\r\n".encode())

    def hotStart(self):
        """ Restart the GPS module making use of previously cached data """
        self.ser.write("$PMTK101*32\r\n".encode())
#########################################################################

    #Methods to get different NMEA message types from GPS module:


    def getRMC(self):
        """ Read a GPRMC NMEA message """
        nmea_msg = ''
        while nmea_msg[0:6] != '$GPRMC':
            nmea_msg = self.ser.readline().decode()
            nmea_msg = nmea_msg[0:len(nmea_msg)-2] #exclude <CR><LF> when parsing
        nmea_obj = nmea.parse(nmea_msg)
        return nmea_obj

    def getVTG(self):
        """ Read a GPVTG NMEA message """
        nmea_msg = ''
        while nmea_msg[0:6] != '$GPVTG':
            nmea_msg = self.ser.readline().decode()
            nmea_msg = nmea_msg[0:len(nmea_msg)-2] #exclude <CR><LF> when parsing
        nmea_obj = nmea.parse(nmea_msg)
        return nmea_obj

    def getGGA(self):
        """ Read a GPGGA NMEA message """
        nmea_msg = ''
        while nmea_msg[0:6] != '$GPGGA':
            nmea_msg = self.ser.readline().decode()
            nmea_msg = nmea_msg[0:len(nmea_msg)-2] #exclude <CR><LF> when parsing
        nmea_obj = nmea.parse(nmea_msg)
        return nmea_obj

    def getGSA(self):
        """ Read a GPGSA NMEA message """
        nmea_msg = ''
        while nmea_msg[0:6] != '$GPGSA':
            nmea_msg = self.ser.readline().decode()
            nmea_msg = nmea_msg[0:len(nmea_msg)-2] #exclude <CR><LF> when parsing
        nmea_obj = nmea.parse(nmea_msg)
        return nmea_obj

    def getGSV(self):
        """ Read a GPGSV NMEA message """
        nmea_msg = ''
        while nmea_msg[0:6] != '$GPGSV':
            nmea_msg = self.ser.readline().decode()
            nmea_msg = nmea_msg[0:len(nmea_msg)-2] #exclude <CR><LF> when parsing
        nmea_obj = nmea.parse(nmea_msg)
        return nmea_obj

    def getGLL(self):
        """ Read a GPGLL NMEA message """
        nmea_msg = ''
        while nmea_msg[0:6] != '$GPGLL':
            nmea_msg = self.ser.readline().decode()
            nmea_msg = nmea_msg[0:len(nmea_msg)-2]  #exclude <CR><LF> when parsing
        nmea_obj = nmea.parse(nmea_msg)
        return nmea_obj

    def continuousRead(self):
        """ Continously print raw NMEA messages to terminal """
        while True:
            try:
                print(self.ser.readline().decode())
                sleep(0.1)
            except KeyboardInterrupt:
                break

    def getPQEPE(self):
        """ Read a PQEPE NMEA message. URC messages have to be enabled first in order to use this. """
        nmea_msg = ''
        while nmea_msg[0:6] != '$PQEPE':
            nmea_msg = self.ser.readline().decode()
            nmea_msg = nmea_msg[0:len(nmea_msg)-2]  #exclude <CR><LF> when parsing
        #nmea_obj = nmea.parse(nmea_msg)
        print(nmea_msg)

    def getNumSats(self):
        """ Return how many satellites are currently being used in receiving GPS data """
        nmea_obj = self.getGGA()
        num_sats = nmea_msg.num_sats
        print(num_sats)
        return num_sats

    def getLongLat(self, gll):
        """ Return the current longitude and latitude coordinates as a string

            arguments:
            gll -- pynmea2 NMEA object for a GPGLL message
            """
        #nmea_obj = self.getGLL()
        nmea_obj = gll
        res = str(nmea_obj.latitude) + ',' + nmea_obj.lat_dir + ','+ str(nmea_obj.longitude) + "," + nmea_obj.lon_dir
        return res

    def getAltitude(self):
        """ Determine current altitude """
        nmea_obj = self.getGGA()
        alt = nmea_obj.altitude
        return alt


#######################################################################################3
#Methods for the Distance Matrix API:
#######################################################################################3


    def distanceTo(self, dst_lat, dst_long):
        """ Determine distance from current coordinates to an entered set of coordinates.

        arguments:
        dst_lat -- latitude coordinates of destination
        dst_long -- longitude coordinates of destination
        """
        data = self.getGLL()
        origin_lat = data.latitude
        origin_long = data.longitude
        return GPS.distanceFromTo(origin_lat, origin_long, dst_lat, dst_long)

    #set Google API key:
    @classmethod
    def setAPIKey(cls, key):
        """ Temporarily save user's Google Maps Distance Matric API key as class attribute for duration of program

        arguments:
        key -- user's Google API key as a setwarnings
        """
        GPS.API_KEY = key


    @classmethod
    def distanceFromTo(cls, origin_lat, origin_long, dst_lat, dst_long):
        """ Get distance from entered source coordinates to entered destination coordinates

        arguments:
        origin_lat -- latitude coordinates of source location
        origin_long -- longitude coorindates of source location
        dst_lat -- latitude coordinates of destination location
        dst_long -- longitude coordinates of destination location
        """

        url1 = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        url2 = 'origins='+str(origin_lat) + ',' + str(origin_long)
        url3 = '&destinations=' +str(dst_lat) + ',' + str(dst_long)
        url4 = "&mode=car&key=" + GPS.API_KEY
        url = url1 + url2 + url3 + url4
        output = requests.get(url).json()    #sending get request to google maps Distance MatriX API
        return output["rows"][0]["elements"][0]["distance"]["value"]



#used for testing
if __name__ == "__main__":
    pass
