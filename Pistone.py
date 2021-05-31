#importiamo le librerie per il controllo dell'interfaccia GPIO
import RPi.GPIO as GPIO
import time
import sys
import unittest
#import pydevd
#from datetime import datetime, date, time, timezone
import Analogscan
#import threading
#from datetime import date
#import time
#from pytime import time
import _thread
#import thread
#import threading
import time
import  subprocess
import os
# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# Create two threads as follows
#try:
#   _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#   _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
#except:


#print "time.time(): %f " %  time.time()
#print time.localtime( time.time() )
ts=0
def Analog(threadName, ciclo):
    print('Analog\n')
    global ts
    ts=ts+1
    A=Analogscan.AnScan(low_channel=0,high_channel=15,rat=15000,samples=(15000*16*5))
    j=0
    plotting=False
    print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
    #T=("%f"%  pytime.timestamps())
    #T=("%f"%ciclo)
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
        #z="/home/pi/demo%d"%ciclo
        #z=z+".txt"
        #f = open(z, "w")
        #i=0
        #while(i<len(R[0])):
        #    f.write(" %f\n" %R[0][i])
        #    i=i+1
        #f.close()
        print("z is",z)
        #subprocess.run(["scp", z, "novello@10.16.1.208:/home/novello"])
        #subprocess.run(['rm','-rf',z])
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
        subprocess.call(["scp", z, "novello@10.16.1.208:/home/novello"])
    return

 

#for i in range(3):
#    t = threading.Thread(target=Analog)
#    t.start()

'''
#definiamo che pinLedLeft e pinLedRight sono due pin di output
#!/usr/bin/env python3
import signal
import sys
import RPi.GPIO as GPIO
BUTTON_GPIO = 16

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
    
def button_pressed_callback(channel):
    print("Button pressed!")
    
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
'''
class PistoneRPi():
    def __init__(self,Debug=0,S=[1,2],P=[18,17]):
        GPIO.setmode(GPIO.BCM)
        print("Init")
        self.S=S
        self.P=P
        print("S[0] is sensore basso")
        print("S[1] is sensore alto")
        i=0
        while(i<len(self.S)):
            GPIO.setup(self.S[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            print("pin In Ingresso is",S[i])
            i=i+1
        i=0
        while(i<len(P)):
            GPIO.setup(self.P[i] , GPIO.OUT)
            print("PIN IN OUT IS ",P[i])
            i=i+1
        print("PreLoad")
        self.setPin(self.P[1],0)
        self.setPin(self.P[0],0)    
        return
        i=0
        '''
         ATTENZIONE SECONDO INDICAZIONI DI GIULIANO LO POSTO PRIMA SU  PERC
         ATTENZIONE NON PARTE BENE......
         
        '''
        if(self.getPin(self.S[1])==0):
            print("UP INIT PHASE ==============>>>>S[1] is 0")
            while(self.getPin(self.S[0])==0):#attenzione magnetico 
                self.setPin(self.P[1],1) ##DOWN
                self.setPin(self.P[0],0)
                time.sleep(1)
                print("init")
                self.setPin(self.P[1],0) ##DOWN
                self.setPin(self.P[0],1)
                time.sleep(1)
                #time.sleep(0.05)
                #print("UP S0 is",self.getPin(self.S[0]))
                #print("UP S1 is",self.getPin(self.S[1]))
                #print("i up is",i)
                #time.sleep(0.3)
                i=i+1
        '''
        # mi devo portare in posizione fissa....
        while((self.getPin(self.S[0])==0)and(self.getPin(self.S[1])==0)):
            self.setPin(self.P[1],1)  #UP
            self.setPin(self.P[0],0)
            time.sleep(0.4)
            self.setPin(self.P[1],0) #DOWN
            self.setPin(self.P[0],1)
            print("S0",self.getPin(self.S[0]))
            print("S1",self.getPin(self.S[1]))
            time.sleep(0.5)
            i=i+1
            print(i)
        print("S0",self.getPin(self.S[0]))
        print("S1",self.getPin(self.S[1]))
        '''
    def Up(self):  #se magnetici
        i=0
        if(self.getPin(self.S[1])==1):
            print("UP S[1] is 1")
            while(self.getPin(self.S[0])==0):
                self.setPin(self.P[1],1)
                self.setPin(self.P[0],0)
                #print("UP S0 is",self.getPin(self.S[0]))
                #print("UP S1 is",self.getPin(self.S[1]))
                #print("i up is",i)
                #time.sleep(0.3)
                i=i+1
        else:
            print("UP Enabled ? S[1] is",self.S[1])
        return(self.getPin(self.S[0]),self.getPin(self.S[1]))

    def Down(self):
        i=0
        if(self.getPin(self.S[0])==1):
            print("Down s[0]=1")
            while(self.getPin(self.S[1])==0):
                self.setPin(self.P[1],0)
                self.setPin(self.P[0],1)
                #print("DOWN S0 is",self.getPin(self.S[0]))
                #print("DOWN S1 is",self.getPin(self.S[1]))
                #print(" i down is",i)
                #time.sleep(0.3)
                i=i+1
        else:
            print( "DOWN s[0] is".self.S[0])
        return(self.getPin(self.S[0]),self.getPin(self.S[1]))
    def Ciclo(self):
        pass
    
    def __del__(self):
        print("Close tasti")
        
    def setPin(self,inp,value):
        if(value==1):
            GPIO.output(inp,GPIO.HIGH)
        else:
            GPIO.output(inp,GPIO.LOW)
            
    def getPin(self,inp):
        return GPIO.input(inp)
        
    # in posizione 0 UP
    # in posizione 1 DOWN
    
def main():
    #pydevd.settrace('192.168.1.62') # replace IP with address
    print("Start")
    global ts
    P1=PistoneRPi(S=[19,20],P=[17,18]) #UP AND DOWN
    P2=PistoneRPi(S=[6,16],P=[24,25])
    k=0
    i=0
    while(i<10):
       print("S[0] is",P1.getPin(P1.S[0]))
       print("S[1] is",P1.getPin(P1.S[1]))
       i=i+1
      
    #print(P1.Up())
    print(P1.Down())
    
    ts=0
    while(k<0):
        #print(" k is",k)
        #print("s0",P1.getPin(P1.S[0]))
        #print("s1",P1.getPin(P1.S[1]))
        P1.Down()
        #time.sleep(0.1)
        P2.Up()
        P2.Down()
        P2.Up()
        #time.sleep(0.1)
        P1.Up()
        #P1.Down()
        #time.sleep(1)
        if((k%1000)==0):
            print("Ciclo is",k)
            #t = threading.Thread(target=Analog)
            #t.start()
            #_thread.start_new_thread( Analog, ("A2dconv", ts, ) )
            ts=ts+1
        k=k+1
        #print("Ciclo is",k)
    print("Fine")
     #######
if __name__ == '__main__':
    main()
