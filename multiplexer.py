# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 09:35:17 2023

@author: WAVELABS-R90VZ50M
"""

import serial
import time

m1_ON="AA0100000000BB"
m1_OFF="AA0100000100BB"
m2_ON="AA0101000000BB"
m2_OFF="AA0101000100BB"
m3_ON="AA0102000000BB"
m3_OFF="AA0102000100BB"
m4_ON="AA0103000000BB"
m4_OFF="AA0103000100BB"
m5_ON="AA0104000000BB"
m5_OFF="AA0104000100BB"
m6_ON="AA0105000000BB"
m6_OFF= "AA0105000100BB"
ser1=serial.Serial(port='COM5',baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)
def muxoperation(value):
    f = bytes.fromhex(value)
    ser1.write(f)
count=1
while count<7:
    muxoperation(m1_ON)
    time.sleep(2)
    muxoperation(m1_OFF)
    count=count+1
    muxoperation(m2_ON)
    time.sleep(2)
    muxoperation(m2_OFF)
    count=count+1
    muxoperation(m3_ON)
    time.sleep(2)
    muxoperation(m3_OFF)
    count=count+1
    muxoperation(m4_ON)
    time.sleep(2)
    muxoperation(m4_OFF)
    count=count+1
    muxoperation(m5_ON)
    time.sleep(2)
    muxoperation(m5_OFF)
    count=count+1
    muxoperation(m6_ON)
    time.sleep(2)
    muxoperation(m6_OFF)
    count=count+1

ser1.close()


