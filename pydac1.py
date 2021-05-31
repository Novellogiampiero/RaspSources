'''
Created on 15 gen 2018

@author: novello
'''
import struct
import os
import sys
import binascii
import sys
import time
import threading
import math
import collections
import logging
import binascii
#import canopen

#import ConfigParser 
import shlex
import subprocess
import logging
import time
#import serial
from threading import Thread
#import devinfo
from ctypes import c_uint8, LittleEndianStructure, Union, c_uint16
import unittest
from ctypes import cdll
import array
libDAC = cdll.LoadLibrary('/home/novello/eclipse-workspace/libdac/Debug/liblibdac.so')
import DigIO

#dac_new() {return new usbdac();}
#bool dac_SetPortA(usbdac * usbdacptr ,unsigned char value ){return usbdacptr->WritePortA(value);}
#bool dac_SetPortB(usbdac * usbdacptr ,unsigned char value ){return usbdacptr->WritePortB(value);}
#bool dac_SetPortC(usbdac * usbdacptr ,unsigned char value ){return usbdacptr->WritePortC(value);}
#unsigned char dac_GetPortA(usbdac * usbdacptr){return usbdacptr->ReadPortA();}
#unsigned char dac_GetPortB(usbdac * usbdacptr){return usbdacptr->ReadPortB();}
#unsigned char dac_GetPortC(usbdac * usbdacptr){return usbdacptr->ReadPortC();}
#bool dac_GetPortCByPin(usbdac * usbdacptr, unsigned char pinnumber){return usbdacptr->PortCReadPin(pinnumber);}
#bool dac_GetPortBByPin(usbdac * usbdacptr, unsigned char pinnumber){return usbdacptr->PortBReadPin(pinnumber);}
#bool dac_GetPortAByPin(usbdac * usbdacptr, unsigned char pinnumber){return usbdacptr->PortAReadPin(pinnumber);}
#bool dac_SetPortCByPin(usbdac * usbdacptr, unsigned char pinnumber,bool value){return usbdacptr->PortcWritePin(pinnumber,value);}
#bool dac_SetPortBByPin(usbdac * usbdacptr, unsigned char pinnumber,bool value){return usbdacptr->PortbWritePin(pinnumber,value);}
#bool dac_SetPortAByPin(usbdac * usbdacptr, unsigned char pinnumber,bool value){return usbdacptr->PortaWritePin(pinnumber,value);}



class DAC(object,):
    def __init__(self,Debug=False):
        self.Debug=Debug
        if(self.Debug):
            self.obj=libDAC.Dac_new()
        else:
            self.Dig=DigIO.Digi()
            
        
        print(" Dac Init")
        
    def __del__(self):
        if(self.Debug):
            libDAC.close(self.obj)
        else:
            self.Dig.__del__()
        print("DAC::del")
       
    def WritePorta(self,value):
        if(self.Debug):
            tmp=libDAC.dac_SetPortA(self.obj,value)
        else:
            self.Dig.Write(0,value)
        return tmp
    
    def WritePortb(self,value):
        if(self.Debug):
            tmp=libDAC.dac_SetPortB(self.obj,value)
        else:
            self.Dig.Write(1,value)
        return tmp
    
    def WritePortc(self,value):
        if(self.Debug):
            tmp=libDAC.dac_SetPortC(self.obj,value)
        else:
            print("Porta C NON USATA")
        return tmp
    
      
    def ReadPorta(self):
        if self.Debug:
            tmp=libDAC.dac_GetPortA(self.obj)
        else:
            tmp=self.Dig.Read(0)
        return tmp

    def ReadPortb(self):
        if(self.Debug):
            tmp=libDAC.dac_GetPortB(self.obj)
        else:
            tmp=self.Dig.Read(1)
        return tmp
      
    def ReadPortc(self):
        if self.Debug:
            tmp=libDAC.dac_GetPortC(self.obj)
        else:
            print("Porta C Not readable")
        return tmp
      
      
    def getPortabypin(self, pinnumber):
        if self.Debug:
            tmp=libDAC.dac_GetPortAByPin(self.obj,pinnumber)
        else:
            print("Non usabile A")
        return tmp
    
    def getPortbbypin(self, pinnumber):
        if(self.Debug):
            tmp=libDAC.dac_GetPortBByPin(self.obj,pinnumber)
        else:
            print("PORTA B NOT USABLE")
        return tmp
    
    def getPortcbypin(self, pinnumber):
        if self.Debug:
            tmp=bytes(1)
            tmp=libDAC.dac_GetPortCByPin(self.obj,pinnumber)
        else:
            print("PORTA B NON USABILE")
        return tmp

    def setPortabypin(self,pinnumber, value):
        if self.Debug:
            print("setPortabypin ")
            #print("pinnumber ",pinnumber)
            tmp=libDAC.dac_SetPortAByPin(pinnumber,value)
        else:
            porta=self.ReadPorta()
            #print("Porta a is   %x ",porta)
            val=(1<<pinnumber)
            #print("Pin selected is %x", value)
            if(value==0):
                porta=(porta & (~val))
                #portaa=portaa & value
            else:
                porta=(porta | val)
            #print("porta at is",porta)
            tmp=self.WritePorta(porta)
        return tmp
      
    def setPortbbypin(self,pinnumber, value):
        if self.Debug:
            tmp=libDAC.dac_SetPortBByPin(pinnumber,value)
        else:
            portb=self.ReadPortb()
            val=(1<<pinnumber)
            if(value==0):
                portb=(portb & (~val))
            else:
                portb=(portb|val)
            tmp=self.WritePortb(portb)
        return tmp
    
    def setPortcbypin(self,pinnumber, value):
        if(self.Debug):
            tmp=libDAC.dac_SetPortCByPin(pinnumber,value)
        else:
            print("NON USABILE")
        return tmp
    
    

def main():
    Da=DAC()
    i=0
    while(i<1000):
        Da.WritePorta(0xff)
        time.sleep(1)
        #i2c.WritePorta(0)
        print(i)
        i=i+1

if __name__ == '__main__':
    main()
