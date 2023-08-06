""" Moisture Sensor Library """

from time import sleep
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import json

class MoistureSensor:
    """ Class to represent moisture sensor object

    Attributes:
    SPI_TYPE -- string to specify the type of SPI configuration used for the MCP3008
    """

    SPI_TYPE = 'HW'

    def __init__(self, datapin, SPI_PORT, adcChannel, pwr_pin ):
        """ Instantiate MoistureSensor object using keyword arguments

        arguments:
        datapin -- integer to represent MISO pin of Raspberry Pi
        SPI_PORT -- Chip Select pin used on Raspberry Pi for MCP3008
        adcChannel -- channel number of MCP3008 which connects to the MISO pin of Raspberry Pi
        pwr_pin -- GPIO pin number (BCM) used to provide power to moisture sensor
        """
        self.datapin = datapin
        self.SPI_PORT = SPI_PORT
        self.SPI_DEV = SPI_PORT
        self.adcChannel = adcChannel
        self.pwr_pin = pwr_pin
        self.dly = 0.1
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM) # use broadcom pin numbering
        GPIO.setup(self.pwr_pin, GPIO.OUT) # set pin to output mode

        #retrieve saved  min and max settings from configuration file:
        with open('config.json', 'r') as f:
            try:
                data = json.load(f) #try remove self
                self.MAX_READING = data["moisture_sensor"]["max"]
                self.MIN_READING = data["moisture_sensor"]["min"]
            except:
                pass
            f.close()

        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEV))

    def set_pwr_pin(self,pin_num):
        """ Method to change which pwr_pin is used for the moisture sensor

        arguments:
        pin_num -- new pin number being used """
        self.pwr_pin = pin_num

    def setDelay(self, delay):
        """ Method to set the wait time after reading the moisture sensor

        arguments:
        delay -- wait time after reading moisture Sensor
        """
        self.dly = delay
    def setPin(self, pin):
        self.datapin = pin #set data pin to be something else if another microcontroller is used with a serial connection

    def init_SPI(self):
        """ Method to initialise SPI communication with ADC """
        self.SPI_TYPE = 'HW'    #Adafruit_GPIO allows software or hardware SPI. We are using hardware
        self.SPI_PORT = 0       #using CE0 port on pi
        self.SPI_DEV = 0
        mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEV))



    def calibrate_max(self):    #user must submerge sensor in water
        """ Method to set the max moisture value to represent 100% """
        #self.MAX_READING = mcp.read_adc(self.adcChannel)
        max = self.mcp.read_adc(self.adcChannel)
        self.MAX_READING = int(max)
        with open('config.json') as f:
            data = json.load(f)
            data["moisture_sensor"]["max"] = int(max)
        with open('config.json', 'w') as h:
            try:
                json.dump(data,h)
            except:
                print("Something went wrong")
        f.close()

    def calibrate_min(self):     #user must submerge sensor in water
        """ Method to set the min moisture value to represent 100% """
        #self.MIN_READING = mcp.read_adc(self.adcChannel)
        min = self.mcp.read_adc(self.adcChannel)
        self.MIN_READING = int(min)
        with open('config.json') as f:
            data = json.load(f)
            data["moisture_sensor"]["min"] = int(min)
            f.close()
        with open('config.json', 'w') as h:
            try:
                json.dump(data,h, indent==2)
            except:
                print("Something went wrong")
        f.close()


    def singleRead(self):
        """ Method to take a single moisture reading from moisture sensor

        return:
        moisture reading as integer
        """
        GPIO.output(self.pwr_pin, GPIO.HIGH)
        val = self.mcp.read_adc(self.adcChannel)
        sleep(self.dly)
        GPIO.output(self.pwr_pin, GPIO.LOW)
        moisture = ((val-self.MIN_READING)/(self.MAX_READING - self.MIN_READING))*100 #converts to percentage
        return moisture

    @classmethod
    def createRange(cls, min, max, profile_name):
        """ Method to create a moisture range

        arguments:
        min -- min moisture value
        max -- max moisture value
        profile_name -- name of profile range
        """
        new_entry = {profile_name: [min, max]}
        with open('config.json') as f:
            data = json.load(f)
            temp = data["moisture_sensor"]["ranges"]
            f.seek(0)
            temp.update(new_entry)
        with open('config.json', 'w') as h:
            try:
                json.dump(data,h, indent=4)
            except:
                print("Something went wrong")

if __name__ == "__main__":
    pass
