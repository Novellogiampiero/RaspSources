#importiamo le librerie per il controllo dell'interfaccia GPIO
import time
import sys
import unittest
import time
import  subprocess
import os
from datetime import date
import signal
import sys
import RPi.GPIO as GPIO
end=time.time()

def Dateis():
   today = date.today()
   # dd/mm/YY
   d1 = today.strftime("%d/%m/%Y")
   ##print("d1 =", d1)
   # Textual month, day and year	
   d2 = today.strftime("%B %d, %Y")
   ##print("d2 =", d2)
   # mm/dd/y
   d3 = today.strftime("%m/%d/%y")
   ##print("d3 =", d3)
   # Month abbreviation, day and year	
   d4 = today.strftime("%b-%d-%Y")
   ###print("d4 =", d4)
   return d4
def LoopPeriod(timeout=1):
   global end
   start = time.time()
   delta = start-end
   end = start
   if(delta<timeout):
      return 0,delta
      print("took %.2f seconds to process" % delta)
   else:
      return 1,delta

BUTTON_GPIO = 16

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
    
def button_pressed_callback(channel):
    print(" ALLARME SIAMO BORGHESI")
    
def InterruptEnable(Gpio=16):
   try:
      import RPi.GPIO as GPIO
      GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)
      signal.signal(signal.SIGINT, signal_handler)
   except:
      print("Board sbagliata")
'''
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

'''

def main():
    print(" la data cooorente is",Dateis())
    i=0
    while(i<100):
       time.sleep(0.25)
       LoopPeriod()
       i=i+1
     #######
if __name__ == '__main__':
    main()
