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
import Safetycheck
import pyjson2
#import email
#import database
#definizione delle funzioni
NomeTest="PrimoTestG"
NumeroTot=10
NumeroParziale=10
Nodo="RASPBERRY4-1"
Dataais=""
ts=0

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

Dataais=0
#print "time.time(): %f " %  time.time()
#print time.localtime( time.time() )
ts=0
def Analog(threadName, ciclo):
   print('Analog\n')
   global NomeTest
   global NumeroTot
   global NumeroParziale
   global Nodo
   global ts
   global Dataais
   ts=ciclo
   A=Analogscan.AnScan(low_channel=0,high_channel=15,rat=15000,samples=(15000*16*5))
   j=0
   plotting=False
   #print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
   #T=("%f"%  pytime.timestamps())
   #T=("%f"%ciclo)
   time.sleep(10)
   R=A.doScan()
   while(j<16):
      #x=[]
      #print("len is",len(R[0]))
      #print("A rate is",A.rate)
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
      #NomeTest=NomeTest
      Articolo="Articolo1"
      data=Dataais
      BitQuant=16
      NumeroCiclo=ts
      ciclos=("%d"%ts)
      print("Ciclo is",ciclos)
      kk=0
      while(kk<(15-0+1)):
         DescrizIngresso="A2D%d"%kk
         filename=NomeTest+"_"+DescrizIngresso+"_"+Articolo+"_"+data+"_"+ciclos+"_"+Nodo+".json"
         z=NomeTest+"_"+DescrizIngresso+"_"+Articolo+"_"+data+"_"+ciclos+"_"+Nodo+".txt"
         print(z)
         print(filename)
         Banda=4000 #filtro HW
         Fc=(15000)
         NumeroCampioni=(15000*16*5)
         Errori="OK"
         #print("filename")
         #z="/home/ubuntu/demo%d"%ciclo
         #z=z+".txt"
         f = open(z, "w")
         i=0
         while(i<len(R[kk])):
            f.write(" %f\n" %R[kk][i])
            i=i+1
         f.close()
         print("z is",z)
         pyjson2.TestParameterWr(filename,NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,Dati=R[kk])
         subprocess.call(["scp", filename, "lab1@10.16.81.250:/home/lab1/Test1"])
         subprocess.run(["scp", z, "lab1@10.16.81.250:/home/lab1/Test1"])
         subprocess.run(['rm','-rf',z])
         subprocess.run(['rm','-rf',filename])
         kk=kk+1
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
      # Set up GPIO pins
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
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
      print("iNIZIALIZZO A 0 ")
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
            print("Mouvo pistoni test")
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
         #print("UP S[1] is 1")
         while(self.getPin(self.S[0])==0):
            self.setPin(self.P[1],1)
            self.setPin(self.P[0],0)
            #print("UP S0 is",self.getPin(self.S[0]))
            #print("UP S1 is",self.getPin(self.S[1]))
            #print("i up is",i)
            #time.sleep(0.3)
            i=i+1
      else:
         print("UP Enabled ? S[1] is",self.getPin(self.S[1]))
      #self.setPin(self.P[1],0)
      #self.setPin(self.P[0],1)
      return(self.getPin(self.S[0]),self.getPin(self.S[1]))

   def Down(self):
      i=0
      if(1):#self.getPin(self.S[0])==1):
         #print("Down s[0]=1")
         while(self.getPin(self.S[1])==0):
            self.setPin(self.P[1],0)
            self.setPin(self.P[0],1)
            #print("DOWN S0 is",self.getPin(self.S[0]))
            #print("DOWN S1 is",self.getPin(self.S[1]))
            #print(" i down is",i)
            #time.sleep(0.3)
            i=i+1
      else:
         pass
         #print( "111111DOWN s[0] is",self.getPin(self.S[0]))
      #self.setPin(self.P[1],1)
      #self.setPin(self.P[0],0)
      return(self.getPin(self.S[0]),self.getPin(self.S[1]))

   def Ciclo(self):
      pass
    
   def __del__(self):
      self.setPin(self.P[1],0)
      self.setPin(self.P[0],0)    
      print("Close tasti")
        
   def setPin(self,inp,value):
      if(value==1):
         GPIO.output(inp,GPIO.HIGH)
      else:
         GPIO.output(inp,GPIO.LOW)
            
   def getPin(self,inp):
      if(GPIO.input(inp)==True):
         return 1
      else:
         return 0
        
    # in posizione 0 UP
    # in posizione 1 DOWN
    
def main():
   AAUTOMATICO=27
   UUP=22
   DDOWN=23
   GIALLO=13
   LED1=26
   LED2=12
   time.sleep(30)
   global ts
   global NomeTest
   global NumeroTot
   global NumeroParziale
   global Nodo
   global RefDB
   global Dataais
   # DB=database.db()
   #try:
   #DB.MakeTestParameterTable("TestGiuliano3")
   #except:
   #print("Attnzione la tabella esiste")
   Dataais=Safetycheck.Dateis()
   Articolo="DeviatoriLeveta"
   Nome,NumeroTot,NumeroParziale,Nodo=pyjson2.ReadConfig("ttt.json")
   NomeTest=nome
   print("Nome del test is",Nome)
   print("data is",Dataais)
   print("NomeArt is",Articolo)
   #RefDB=DB.InsertParameterInRefTable("TestGiuliano3",NomeTest=Nome,datastarttest=Dataais, Articolo="BOOO",Nodo=Nodo,Numerodibit=16,Banda=4000,Fc=15000)
   #print("RefDB is",RefDB)
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(LED2 , GPIO.OUT)#led2
   GPIO.setup(LED1 , GPIO.OUT)#led1
   GPIO.setup(GIALLO,GPIO.OUT)#led giallo
   GPIO.setup(AAUTOMATICO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#AUTOMATICO
   GPIO.setup(UUP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#UP
   GPIO.setup(DDOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#DOWN
   #print("pin In Ingresso is",S[i])
   GPIO.setwarnings(False)
   global ts
   P1=PistoneRPi(S=[5,6],P=[17,18]) #UP AND DOWN
   #P2=PistoneRPi(S=[6,16],P=[24,25])
   k=0
   i=0
   while(i<0):
      print("S[0] is",P1.getPin(P1.S[0]))
      print("S[1] is",P1.getPin(P1.S[1]))
      i=i+1
   i=0
   #print(P1.Up())
   while(i<2):
      time.sleep(0.05)
      P1.setPin(P1.P[0],1)
      P1.setPin(P1.P[1],0)
      time.sleep(0.03)
      P1.setPin(P1.P[0],0)
      P1.setPin(P1.P[1],1)
      i=i+1
   
   #print(P1.Down()) 
   ts=0
   while(not GPIO.input(AAUTOMATICO)):
      print("NON AUTOMATICO")
      if(GPIO.input(UUP)):
         P1.Up()
      if(GPIO.input(DDOWN)):
         P1.Down()
      time.sleep(0.2)
   #while(not GPIO.input(UUP)):
   #   time.sleep(1)
      
   time.sleep(1)
   while(k<NumeroTot):
      print(" k is",k)
      #print("s0",P1.getPin(P1.S[0]))
      #print("s1",P1.getPin(P1.S[1]))
      P1.Down()
      #if(GPIO.input(DDOWN)):
      #return
      #time.sleep(0.1)
      #P2.Up()
      #P2.Down()
      Ok,t=Safetycheck.LoopPeriod(timeout=10)
      print(t)
      if(Ok==1):
         print("Errore timeout")
         #return 1
      if((k & 0X01)==1):
         GPIO.output(12,GPIO.HIGH)
      else:
         GPIO.output(12,GPIO.LOW)
      #P2.Up()
      #time.sleep(0.1)
      P1.Up()
      #P1.Down()
      #time.sleep(1)
      if((k%NumeroParziale)==50):
         print("Ciclo is",k)
         #t = threading.Thread(target=Analog)
         #t.start()
         _thread.start_new_thread( Analog, ("A2dconv", k, ) )
         ts=ts+1
      k=k+1
      #print("Ciclo is",k)
   print("Fine")
#######
if __name__ == '__main__':
    main()
   
