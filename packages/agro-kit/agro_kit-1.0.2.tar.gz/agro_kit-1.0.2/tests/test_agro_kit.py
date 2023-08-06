#!/usr/bin/env python

"""Tests for `agro_kit` package."""

import pytest
from agro_kit.agro_kit import AgroKit
import pynmea2 as nmea

myAG = AgroKit()  #initialise AgroKit object
gll = "$GPGLL,4916.45,N,12311.12,W,225444,A,*1D"

def testRMC():
    x = myAG.GPS.getRMC()
    assert x.__class__.__name__ == "RMC"

def testGGA():
    x = myAG.GPS.getGGA()
    assert x.__class__.__name__ == "GGA"

def testGLL():
    x = myAG.GPS.getGLL()
    assert x.__class__.__name__ == "GLL"

def testGSV():
    x = myAG.GPS.getGSV()
    assert x.__class__.__name__ == "GSV"

def testGSA():
    x = myAG.GPS.getGSA()
    assert x.__class__.__name__ == "GSA"

def testVTG():
    x = myAG.GPS.getVTG()
    assert x.__class__.__name__ == "VTG"

def testGetLongLat():
    nmea_obj = nmea.parse(gll)
    res = myAG.GPS.getLongLat(nmea_obj)
    assert res == "49.274166666666666,N,-123.18533333333333,W"

def testLoadProfile():
    myAG.loadProfile("pytest")
    assert myAG.MIN_MOISTURE == 0
    assert myAG.MAX_MOISTURE == 10
    assert myAG.MIN_LUX == 20
    assert myAG.MAX_LUX == 30

def testReadMoisture():
    x = myAG.MS.singleRead()
    assert x.__class__.__name__ == "float"

def testReadLux():
    x = myAG.LS.singleReadLux()
    assert x.__class__.__name__ == "float"

def testReadColour():
    x = myAG.LS.singleReadColour()
    assert x.__class__.__name__ == "float"
