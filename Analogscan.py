"""
Wrapper call demonstrated:        ai_device.a_in_scan()

Purpose:                          Performs a continuous scan of the range
                                  of A/D input channels

Demonstration:                    Displays the analog input data for the
                                  range of user-specified channels using
                                  the first supported range and input mode

Steps:
1.  Call get_daq_device_inventory() to get the list of available DAQ devices
2.  Create a DaqDevice object
3.  Call daq_device.get_ai_device() to get the ai_device object for the AI
    subsystem
4.  Verify the ai_device object is valid
5.  Call ai_device.get_info() to get the ai_info object for the AI subsystem
6.  Verify the analog input subsystem has a hardware pacer
7.  Call daq_device.connect() to establish a UL connection to the DAQ device
8.  Call ai_device.a_in_scan() to start the scan of A/D input channels
9.  Call ai_device.get_scan_status() to check the status of the background
    operation
10. Display the data for each channel
11. Call ai_device.scan_stop() to stop the background operation
12. Call daq_device.disconnect() and daq_device.release() before exiting the
    process.
"""
from __future__ import print_function
from time import sleep
from os import system
from sys import stdout
import time
import subprocess
try:
    import matplotlib.pyplot as plt
except:
    print("NO PLT")
import wave, struct, math
import datetime

'''
NOT USED
sampleRate = 44100.0 # hertz
duration = 1.0 # seconds
frequency = 440.0 # hertz
obj = wave.open('sound.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)
for i in range(99999):
   value = random.randint(-32767, 32767)
   data = struct.pack('<h', value)
   obj.writeframesraw( data )
obj.close()
'''

from uldaq import (get_daq_device_inventory, DaqDevice, AInScanFlag, ScanStatus,
                   ScanOption, create_float_buffer, InterfaceType, AiInputMode)


class AnScan:
    def __init__(self,low_channel=0,high_channel=0,rat=50000,samples=500000):
        """Analog input scan example."""
        self.daq_device = None
        self.ai_device = None
        self.status = ScanStatus.IDLE
        self.range_index = 0
        self.interface_type = InterfaceType.ANY
        self.low_channel = low_channel
        self.high_channel = high_channel
        self.samples_per_channel = samples
        self.rate = rat
        self.scan_options = ScanOption.CONTINUOUS
        self.flags = AInScanFlag.DEFAULT
        self.x = datetime.datetime.now()
        try:
            # Get descriptors for all of the available DAQ devices.
            self.devices = get_daq_device_inventory(self.interface_type)
            number_of_devices = len(self.devices)
            if number_of_devices == 0:
                raise RuntimeError('Error: No DAQ devices found')
            print('Found', number_of_devices, 'DAQ device(s):')
            for i in range(number_of_devices):
                print(self.devices[i].product_name)
                print(self.devices[i].unique_id) 
                # Create the DAQ device from the descriptor at the specified index.
                self.daq_device = DaqDevice(self.devices[i])
            print("A")
            # Get the AiDevice object and verify that it is valid.
            self.ai_device = self.daq_device.get_ai_device()
            if self.ai_device is None:
                raise RuntimeError('Error: The DAQ device does not support analog ''input')
            # Verify the specified device supports hardware pacing for analog input.
            print("B")
            self.ai_info = self.ai_device.get_info()
            
            if not self.ai_info.has_pacer():
                raise RuntimeError('\nError: The specified DAQ device does not ''support hardware paced analog input')
            print("ciao1")
            # Establish a connection to the DAQ device.
            self.descriptor = self.daq_device.get_descriptor()
            print('\nConnecting to', self.descriptor.dev_string, '- please wait...')
            # For Ethernet devices using a connection_code other than the default
            # value of zeo, change the line below to enter the desired code.
            self.daq_device.connect(connection_code=0)
            print("ciao2")

            # The default input mode is SINGLE_ENDED.
            self.input_mode = AiInputMode.SINGLE_ENDED
            
            # If SINGLE_ENDED input mode is not supported, set to DIFFERENTIAL.
            if self.ai_info.get_num_chans_by_mode(AiInputMode.SINGLE_ENDED) <= 0:
                self.input_mode = AiInputMode.DIFFERENTIAL
            

            # Get the number of channels and validate the high channel number.
            print("ciao3")
            number_of_channels = self.ai_info.get_num_chans_by_mode(self.input_mode)
            print("ciao4")
            if high_channel >= number_of_channels:
                high_channel = number_of_channels - 1
            self.channel_count = high_channel - low_channel + 1
            print("ciao 5")

            # Get a list of supported ranges and validate the range index.
            self.ranges = self.ai_info.get_ranges(self.input_mode)
            print("ciao 6")
            if self.range_index >= len(self.ranges):
                self.range_index = len(self.ranges) - 1
            print("ciao 7")

            # Allocate a buffer to receive the data.
            self.data = create_float_buffer(self.channel_count, self.samples_per_channel)
            print("ciao 8")
        except:
            print("errore init")
        #print('\n', self.descriptor.dev_string)
        print('    Function demonstrated: ai_device.a_in_scan()')
        print('    Channels: ', self.low_channel, '-', self.high_channel)
        print('    Input mode: ', self.input_mode.name)
        print('    Range: ', self.ranges[self.range_index].name)
        print('    Samples per channel: ', self.samples_per_channel)
        print('    Rate: ', self.rate, 'Hz')
        print('    Scan options:', self.display_scan_options(self.scan_options))

    def doScan(self,timeout=1000):
        #data = create_float_buffer(channel_count, self.samples_per_channel)
        # Start the acquisition.
        k=0
        i=0
        Result=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        print(self.channel_count)
        #while(k<(self.channel_count)):
        #    Result.append(0)
        #    k=k+1
        #print("Result is",Result)
        rate = self.ai_device.a_in_scan(self.low_channel, self.high_channel, self.input_mode,self.ranges[self.range_index], self.samples_per_channel,self.rate, self.scan_options, self.flags, self.data)
        index=-1
        T=0
        print("SAMPLES PER CHANNEL IS",self.samples_per_channel)
        while(T<(self.samples_per_channel/16)):#era /16
            # Get the status of the background operation
            self.status, transfer_status = self.ai_device.get_scan_status()
            #print("rate is====>>>",self.rate)
            #print("samples per channel",self.samples_per_channel)
            #print('currentTotalCount = ',transfer_status.current_total_count)
            #print('currentScanCount = ',transfer_status.current_scan_count)
            index = transfer_status.current_index
            if(index>0):
                #print('currentTotalCount = ',transfer_status.current_total_count)
                #Limit=transfer_status.current_scan_count
                print('currentIndex = ', index, '\n')
                k=0
                try:
                    while(k<=index):
                        j=0
                        while(j<self.channel_count):
                            Result[j].append(self.data[k+j])
                            j=j+1 
                        k=k+j#1
                except:
                    print("errore nei dati ")
            T=len(Result[0])
            time.sleep(1)
        print("len res is",len(Result))
        return Result
    
    def Sampling(self,Dato):
        R=[]
        step=self.channel_count
        i=0
        while(i<len(Dato)):
            R.append(Dato[i])
            i=i+step
        return R

    def __del__(self):
        if self.daq_device:
            #Stop the acquisition if it is still running.
            #if self.status == ScanStatus.RUNNING:
            #self.ai_device.scan_stop()
            #if self.daq_device.is_connected():
            #    self.daq_device.disconnect()
            #self.daq_device.release()
            print("end")


    def display_scan_options(self,bit_mask):
        """Create a displays string for all scan options."""
        options = []
        if bit_mask == ScanOption.DEFAULTIO:
            options.append(ScanOption.DEFAULTIO.name)
        for option in ScanOption:
            if option & bit_mask:
                options.append(option.name)
        return ', '.join(options)


def main():
    A=AnScan(low_channel=0,high_channel=15,rat=15000,samples=(15000*16))
    j=0
    plotting=False
    while(j<1):
        R=A.doScan()
        #x=[]
        print("len is",len(R[0]))
        print("A rate is",A.rate)
    
        x=[]
        i=0
        while(i<len(R[0])):
            x.append(i/(A.rate))
            i=i+1
        j=j+1
    if(plotting):
        plt.plot(x,R[0])
        plt.plot(x,R[1])
        plt.plot(x,R[8])
        plt.show()
    else:
        filename="/home/pi/demofile2.txt"
        f = open("/home/pi/demofile2.txt", "a")
        i=0
        while(i<len(R[0])):
            f.write(" %f" %R[0][i])
            i=i+1
        f.close()
        subprocess.run(["scp", filename, "novello@10.16.1.101:/home/novello"])
        return
        filename="oscillo"
        filename=filename+".wav"
        sampleRate = A.rate # hertz
        duration = 2.0 # seconds
        frequency = 440.0 # hertz
        obj = wave.open(filename,'w')
        obj.setnchannels(1) # mono
        obj.setsampwidth(2)
        obj.setframerate(sampleRate)
        i=0
        while(i<len(R[0])):
            value = R[0][i]
            data = struct.pack('<h', int(value))
            i=i+1
        obj.writeframesraw( data )
        obj.close()
        subprocess.run(["scp", filename, "novello@10.16.1.101:/home/novello/iot/lava/lava/test-jenkins"])
if __name__ == '__main__':
    main()
    
