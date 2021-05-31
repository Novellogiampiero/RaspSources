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
import canopen 
from pydac1 import DAC
#from pycan import Can
import shlex
import subprocess
import logging
import time
from seriale import SSerial 
from threading import Thread
from ctypes import c_uint8, LittleEndianStructure, Union, c_uint16
import unittest
import array
import SerialeBT
import pydac1
import RPi.GPIO as GPIO
import time



 ###### PORTE IN USCITA 
 # porta a[0] ==>D1 
 # porta a[1] ==>STOP
 # porta a[2] ==>D11
 # porta a[3] ==>D12
 # porta a[4] ==>D13
 # porta a[5] ===>D16
 # porta a[6] ===>> comando 1
 # porta a[7] ====> STOP
     
 # porta b[0] ==>D30  
 # porta b[1] ==>D32 emulo stop in debug
 # porta b[2] ==>D34 emulo led rosso in debug
 # porta b[3] ==>D36 emulo led verde in debug
 # porta b[4] ==>D29 emulo led bianco 1 in debug
 # porta b[5] ==>D31 emulo led bianco 2 in debug
 # porta b[6] ==>D33 emulo led bianco 3 in debug
 # porta b[7] ==>D33 emulo led bianco 4 in debug
 
 
 # PORTE IN INGRESSO
 #PORTC
 #porta c[0] ==> 
 #porta c[1] ==> STOP 
 #porta c[2] ==> Led Rosso
 #porta c[3] ==> Led Verde
 #porta c[4] ==> Led Bianco 1
 #porta c[5] ==> Led Bianco 2
 #porta c[6] ==> Led Bianco 3
 #porta c[7] ==> Led Bianco 4

class Tasti():
    # TAsto messso su IO della raspberry
    # STOP 2 pin selezionabili su lista
    # START 1 PIN Da LISTA
    # GENERIC D Messo su RASPBERRY
    def __init__(self,Debug=False,can=False,Se=True,STOPS=[1,2],STARTS=[],DS=[]):
        self.can=can
        self.Seriale=Se
        self.STOP=STOPS
        self.START=STARTS
        self.D=DS
        self.Tas=pydac1.DAC()        
        GPIO.setmode(GPIO.BCM)
        
        i=0
        while(i<len(STOPS)):
            GPIO.setup(STOPS[i] , GPIO.OUT)
            i=i+1
        i=0
        while(i<len(STOPS)):
            GPIO.output(STOPS[i], GPIO.LOW)
            i=i+1
        i=0
        while(i<len(STARTS)):
            GPIO.setup(STARTS[i] , GPIO.OUT)
            i=i+1
        i=0
        while(i<len(STARTS)):
            GPIO.output(STARTS[i], GPIO.LOW)
            i=i+1
        i=0
        while(i<len(DS)):
            GPIO.setup(DS[i] , GPIO.OUT)
            i=i+1
        i=0
        while(i<len(DS)):
            GPIO.output(DS[i], GPIO.LOW)
            i=i+1
            
	self.Tas=DAC()
        if(self.can):
            self.Ca=Can(Debug=True,Node10=10,Node11=0,Node12=0,Node13=0)
	if(self.Seriale):
	    self.seri=SerialeBT.SSerial()
        self.Debug=Debug
        #self.can=can
        #if(self.can):
            #self.Ca=Can()
        if (not self.Debug):
            print("attenzione devo mettere tutto in uno stato conosciutio")
            print("inizializzo la dac")
	        #self.Tas.WritePorta(0xff)
			#self.Tas.WritePortb(0xff)
        else:
			self.D=DigIO.Digi()
			self.D.Write(0,0xff)
			self.D.Write(1,0xff)
        self.PortaA=0
        self.PortaB=0
        
    def __del__(self):
        print("Tasti::DEL")
        if self.can:
            self.Ca.__del__()
        if(self.Seriale:
            self.seri.__del__()
        #self.Tas.__del__()
        
    def Leds(self,time=10):
        if(self.Seriale):
            print("La lettura avviene via seriale")
        return  self.seri.loopreadLed(self,timeout=time)
        
    #attivo il filo comando 
    def filoon(self ,filocom):
        GPIO.setup(filocom , GPIO.OUT)
        GPIO.output(filocom, GPIO.HIGHT)
        
      
    #disattivo il filo comando
    def filooff(self,filocom):
        GPIO.setup(filocom , GPIO.OUT)
        GPIO.output(filocom, GPIO.LOW)
	
	#abilito la lista completa delle riceventi
    def RxOn(self,ListRx):
        self.RxList=ListRx
        print("RxOn Rx On List is",ListRx)
        i=0
        while(i<len(ListRx)):
            GPIO.setup(ListRx[i] , GPIO.OUT)
            i=i+1
        i=0
        while(i<len(ListRx)):
            GPIO.output(ListRx[i], GPIO.HIGHT)
            i=i+1
			
    #disabilito lista completa della riceventi
    def RxSet(self,val=0,Nr=0):
        if(val==1):
            GPIO.output(self.RxList[Nr], GPIO.HIGHT)
        else:
            GPIO.output(self.RxList[Nr], GPIO.LOW)
        
    def RxOff(self,ListRx):
        self.RxList=ListRx
        print("RxOn Rx Off List is",ListRx)
        i=0
        while(i<len(ListRx)):
            GPIO.output(ListRx[i], GPIO.LOW)
            i=i+1
			

    ''' ritorna lo stato del led verde '''    
    
    ''' comandi di stop ''' 
    def StopPremuto(self):
            self.Stop(1)

    def StopRilasciato(self):
            self.Stop(0)
            
    ''' comandi di accensione '''         
    def Accensione(self):
        self.StopRilasciato()
        self.d1(0)
        time.sleep(1)
        self.d1(1)
        time.sleep(0.5)
        self.d1(0)
        
    def Spegnimento(self):
        self.StopRilasciato()
        self.d1(0)
        time.sleep(1)
        self.StopPremuto()
        time.sleep(5)
        self.StopRilasciato()
        #if self.Debug:
        #    self.Tas.setPortbbypin(2,value)
    ''' viene usato per il tato di  d1 che puo evere diverse funzioni'''
   
    ''' viene usato per mettere un comando in ON oppure in OFF di fatto cambio
    lo stato del rele nella ricevente  viene usato per spedire dei comandi sui dispositivi configurati '''
        
    def Comando1(self, on_off=1):
        print("comando1==> ATTENZIONE E CONNESSO ALLA PORTA B")
        print(" Sto usando tutti i pin della posta b ")
        if(self.Debug):
			self.Tas.setPortbbypin(0, on_off)
		else:
			print("TODO COMANDO1")
        time.sleep(1)
        print("on_off is ",on_off)
        if(self.Seriale):
            print("leggo i dati dalla seriale")
        try:
            if(self.Ca.node10):
                a=self.Ca.read_pdo(self.Ca.node10,1,5)
                print("a is ",a)
        except:
            print("errore accesso node 10 con CAN")
            a=False
        try:
            if(self.Ca.node11):
                b=self.Ca.read_pdo(self.Ca.node11,1,5)
                self.Ca.write_pdo(self.Ca.node11,1)
                print("b is ",b)
        except:
            print(" errore di accesso al nodo 11")
            b=False
        try:    
            if(self.Ca.node12):
                c=self.Ca.read_pdo(self.Ca.node12,1,5)
                print("c is ",c)
        except:
            print("errore di accesso via can al nodo 12")
            c=False
        try:
            if(self.Ca.node13):
                d=self.Ca.read_pdo(self.Ca.node13,1,5)
                self.Ca.write_pdo(self.Ca.node13,1)
                print("d is ",d)
        except:
            print(" errore di accesso al nodo 13 del can")
            d=False
      
        if((a==on_off) and(b==on_off) and (c==on_off)and (d==on_off)):
            print("OK!!!!")
            return True
        else:
            print("NON OK on off is",on_off)
            print("a is",a)
            print("c is ",c)
            print("b is ",b)
            print("d is ",d)      
            return False
        
    
    def Comando2(self, on_off=1):
        print("Comando2")
        print("comando1==> ATTENZIONE E CONNESSO ALLA PORTA B")
        print(" Sto usando tutti i pin della posta b ") 
        self.Tas.setPortbbypin(7, on_off)
        
    def LedBiancoWaitStatus(self):
        if(self.Seriale):
            print("La seriale ogni secondo mi da lo stato dei led banchi...PS è una lista")
	    self.Leds(10)
    '''
	LedBiancoWaitStatus(0,canale1,canale2,canale3,canale4)
    
        1) attivo il selettore  il led bianco lampeggia velocemente
        2)ho led verde che lampeggia veloce ... attivo selettore  d11 ..
        3)d11==> ledBianco 1 lampeggia velocemente
        4)150ms ON 150mS0ff del led bianco
        5) devo passare a led bianco lento premendo tasto d1
    '''
 ###################################################################    
    def SelectMultiUnit(self,ListaCanali):
        NumeroCanaliSelezionati=0
        StatusLed=0
        self.StopRilasciato()
        time.sleep(5)
        print("led verde is SPENTO", self.LedVerde())
        NumeroCanaliSelezionati=len(ListaCanali) # Da Sistemare
        #ATTENZIONE DEVE LAMPEGGIARE
        statoledBianchi=self.LedBiancoWaitStatus(2,canale1,canale2,canale3,canale4)
        self.d1(1)
        time.sleep(1)
        self.d1(0)
        time.sleep(1)
        statoledBianchi=self.LedBiancoWaitStatus()
        time.sleep(1)
        ''' devo avere gia dato d1 in marcia...
         Ricenente in marcia occupata lampeggia led bianco lentaente
         select resta aceso fisso da lento deve diventare fisso'''
        '''da acceso fisso con deselect ==>  passa in blinca lento''' 
           
    def DeselectMultiunit(self,ListaCanali):
        print("Starts DeselectMultiunit ")
        NumeroCanaliSelezionati=0
        statoLedBianco=self.LedBiancoWaitStatus()
        NumeroCanaliSelezionati=len(NumeroCanaliSelezionati)       
        time.sleep(5)
        statoLedBianco=self.LedBiancoWaitStatus()
        print("Stop DeselectMultiunit  i led bianco deve lampeggiare")
        
        
    '''
        collega e apre la connessione con la ricevente
    ''' 
    
        #### aggiungi attesa leg bianco fisso....
    ''' DeselectMultiReceiver()
        DeselectMultiReceiver(self,canale1=11,0,0,0)'''
     
   
    '''se do start se led bianchi doiventano fissi'''
    ''' se premio lo start il led diventa bianco fisso su quelli che sono in link '''
    ''' attezione ... devi fare una modifica sui led bianchi ... in modalità debug ogni secondo
        spedisce una lista [A,A,A,A] con i 4 stati dei led bianchi e quindi sta parte deve essere decodificata
        una cosa simile deve essere fatta sul led verde... che manda fuori indicazione di sullo stato... MARCIA O NO.
    '''
    def checkBlinkBiancoVeloce(self, led):
        bytes=self.LedBianchi(led)
        if(bytes==3):
            print("Led blink veloce")
            return True 
        return False
        
    def checkBlinkVerdeVeloce(self):
        return False
          
    def  Stop(self,value=1):
        #print("Stop is ",value)
        #print(" se stop premuto ==> rele aperto")
        #print(" se stop RILASCIATO ==> rele CHIUSO")
        if(self.Debug):
            i=0
            while(i<len(self.STOP)):
                if(value==0):
                    GPIO.output(self.STOP[i], GPIO.LOW)
                else:
                    GPIO.output(self.STOP[i], GPIO.HIGH)
                i=i+1   

        else:
			if(value==1):
				self.PortaA=self.PortaA+0x03
			else:
				self.PortaA=(self.PartaA & 0xfc)
			self.D.DoWrite(0,PortaA)       
    
    def d1(self,value=1):
        #print("d1 state is ",value)
        if(self.Debug):
            i=0
            while(i<len(self.START)):
                if(value==0):
                    GPIO.output(self.START[i], GPIO.LOW)
                else:
                    GPIO.output(self.START[i], GPIO.HIGH)
                i=i+1   			
        else:
			if(value==1):
				self.PortaA=self.PortaA+1
			else:
				self.PortaA=(self.PortaA & 0xfe)
			self.D.Write(0,PortaA)
			


    def d(self,pin,value=1):
        #print("d1 state is ",value)
        i=0
        while(i<len(self.D)):
            if(value==0):
                GPIO.output(self.START[i], GPIO.LOW)
            else:
                GPIO.output(self.START[i], GPIO.HIGH)
            i=i+1   
      
		
    ''' viene usato per mettere un comando in ON oppure in OFF di fatto cambio
    lo stato del rele nella ricevente  viene usato per spedire dei comandi sui dispositivi configurati '''
     
         #self.checkBlinkBiancoVeloce((canale1-11),(canale2-11),(canale3-11),(canale4-11))
        
        
    
        
    ''' is a pulsante se viene premuto a seconda dello stato puo avere diverse funzioni'''
    ''' a) usato per acquisire chiave se  stop premuto'''
    ''' b) usato per acquisire mac address  alla fine spegne il tx '''
    ''' c) per mettere in marcia il dispositivo ''' 
    '''liberare ricevente ... va giu link occupa e statrt '''
    ''' dal d11 al d16 '''  
    ''' vengono attivati uno a 1 per ablilitare il conportamento di uno o dell' altro..'''    
    '''  i valori consentiti sono da 11 a 14'''
        
 
#####################FUNZIONI NUOVE        
    ''' a)con stop non attivo
        b)premo d1
        c)e tengo premuto fino a primo led verde premo stop e tempo premto sempre d1 
        d) fino a quando non si spegne '''
    '''si spegne led verde e rosso ==> sapento sistema'''
    ''' rilasciare lo stop '''
    ''' premi d1 fino a che non va di nuovo in autospegnimento .. led rosso off'''
    def Occupa(self,ListaOccupa,Stato=1,Delay=5,Monostabile=True):
        i=0
        while(i<len(ListaOccupa)):
            print("Im using PORT  B")
            if self.Debug:
				self.Tas.setPortbbypin(ListaOccupa[i], Stato)
            else:
				print("Occupa non implementata")
            if Monostabile:
                print(" Occupa",ListaOccupa[i])
                starttimeis=time.ctime();
                print("Start occupa_libera: %s" % starttimeis)
                time.sleep( Delay )
                print( "End : %s" % time.ctime())
                if(self.Debug):
					self.Tas.setPortbbypin(ListaOccupa[i], 0)
                else:
					print("Occupa to do ")
                stoptimeis=time.ctime()
                print("Stop occupa_libera: %s" % stoptimeis)
                #print("Durata is",(stoptimeis-starttimeis))
            i=i+1
    '''
    libera i canali.... attenzione i dx viene data una lista opportuna...
    '''
    def Libera(self,ListaLibera,Stato=1,Delay=5,Monostabile=True):
        i=0
        while(i<len(ListaLibera)):
            print("Im using PORT  B")
            if(self.Debug):
				self.Tas.setPortbbypin(ListaLibera[i], Stato)
            else:
				print("TODO")
            if Monostabile:
                print("Libera is ",ListaLibera[i])
                starttimeis=time.ctime();
                print("Start occupa_libera: %s" % starttimeis)
                time.sleep( Delay )
                print( "End : %s" % time.ctime())
                if self.Debug:
					self.Tas.setPortbbypin(ListaLibera[i], 0)
                else:
					print("Libera non readi")
                stoptimeis=time.ctime()
                print("Stop occupa_libera: %s" % stoptimeis)
                #print("Durata is",(stoptimeis-starttimeis))
            i=i+1
    ''' DeselectMultiReceiver()
        DeselectMultiReceiver(self,canale1=11,0,0,0)
        Seleziona i ricevitori opportuni ....
    '''
    def Select(self,ListaSelect,Stato=1 ,Delay=5,Monostabile=False):
        i=0
        while(i<len(ListaSelect)):
            print("Im using PORT  B")
            if(self.debug):
				self.Tas.setPortbbypin(ListaSelect[i],Stato )
            else:
				print("Select")
            if Monostabile:
                print("select is",ListaSelect[i])
                starttimeis=time.ctime();
                print("Start occupa_libera: %s" % starttimeis)
                time.sleep( Delay )
                print( "End : %s" % time.ctime())
                self.Tas.setPortbbypin(ListaSelect[i], not Stato)
                stoptimeis=time.ctime()
                print("Stop occupa_libera: %s" % stoptimeis)
                #print("Durata is",(stoptimeis-starttimeis))
            i=i+1
              
    def CancellazioneMacAddress(self,timeout=100):
        print(" toglire i rx   vanno spenti,,,,")
        self.StopPremuto()
        time.sleep(1)
        self.StopRilasciato()
        time.sleep(1)
        self.d1(1)
        time.sleep(0.5)#devo aspettare un lampeggio verde!!!
        print("led verde is Blink", self.LedVerde())
        self.StopPremuto()
        #print(self.waitLedRossoOn())
        #self.waitLedRossoGoOff(5) #10 secondi
        time.sleep(10)
        print("Start CancellazioneMacAddress : %s" % time.ctime())
        self.d1(0);
        time.sleep(5)
        self.StopRilasciato()
        time.sleep(1)
        self.d1(1)
        i=0
        while(i<120):
            time.sleep(1)
            print("i is",i)
            i=i+1
        print("ADD TO CHECK")
        self.WaitLedRossoon(100) #circe 30 o di piu secondi 1
        self.waitLedRossooff(100) # 10 secondi
        self.d1(0)
        self.StopPremuto()
        print("Stop CancellazioneMacAddress : %s" % time.ctime())
    
    def Inquiryng(self):
        return  self.GetMackAddress()
        
    #PROCEDURA DI INQUARING
    def GetMackAddress(self):
        self.StopRilasciato()
        result=0
        time.sleep(10)
        # attendi self.LedVerdeBlinkVeloce()
        print("Start GetMackAddress : %s" % time.ctime())
        self.d1(1)
        time.sleep(10)
        print("led verde is Blink lento", self.LedVerde())
        self.d1(0)
        i=0
        while(i<120): #sono 120 secondi 
            if(self.Se):
                SerResult=self.seri.readstring()
                print("Blue Tooth inquiring is",SerResult)
                #attenzione posso riconosce la stringa.... che mi dice OK
                #oppure non OK....
            i=i+1
            
        result+=self.WaitLedRossoon()
        ''' aspetta chee si accenda led rosso e poi partira con lampeggio veloce '''
        result+=self.waitLedRossooff()
        #devo aspettare che si spenga
        
        self.StopPremuto()
        print("sTOP GetMackAddress : %s" % time.ctime())
        if(self.Debug)==2:
            return 1
        else:
            return 0 
        
        
    def AcquisizioneMAckaddressdallarete(self):
        #attenzione prima bisogna accendere le riceventi
        result=0
        self.StopRilasciato() 
        print("Sono in debug mode")
        print("Start AcquisizioneMAckaddressdallarete : %s" % time.ctime())
        print(" Led verde blinca lento ",self.LedVerde())        
        '''    led verde  in debug self.tasti.d1(0)lampeggia lento  '''
        
        self.d1(1)
        time.sleep(1)
        self.d1(0)
        #self.WaitLedVerdeBlinkVeloce()
        print("Finita acquisizione del MAC address")
        result=result+self.WaitLedRossoon()
        ''' aspetta chee si accenda led rosso e poi partira con lampeggio veloce '''
        result=result+self.waitLedRossooff()
        ''' il mac addres e scritto eeprom micro le riceventi se visibili ti danno nome e mac address '''
        print("Start AcquisizioneMAckaddressdallarete : %s" % time.ctime())
        self.StopPremuto()
        if(result==2):
            return 1
        else:
            return 0
        '''    '''
        '''per verificare se buon fine..... mndare in masrcia e deve andare in marcia con led lento '''
    def CancelazioneChiave(self):
        print(" non possibile in eeprom estrerna");
        print(" ERRORE  .... EPROM NON E' SCRIVIBILE");
        pass
    
    '''check stop
        stop premuto
        self.d1(1)
        aspetti 5 sei secondi sparisce alimentazine aspetto spegnimento
         led verde blink ogni secondo  300ms
         blink una volta al secondo per riconoscere spemimentio
    '''    
    def KeyImpprinting(self):
        self.StopPremuto()
        time.sleep(1)
        self.d1(1)
        print("Start KeyImpprinting : %s" % time.ctime())
        print("waiting led roso On ",self.WaitLedRossoon())
        print(" Led rosso on")
        print(" waiting led rosso off",self.waitLedRossooff())
        print("Led rosso off")
        time.sleep(1)
        self.WaitLedRossoon()
        ''' aspetta chee si accenda led rosso e poi partira con lampeggio veloce '''
        self.waitLedRossooff()
        time.sleep(1)
        '''wait autospegnimento ... led rosso si spegne o su led verde '''
        self.d1(0)
        print("Stop KeyImpprinting : %s" % time.ctime())
        print("fatto auto spegnimento")
        self.StopRilasciato()
    '''
     chechk stop
     mi serve pin di auto spegnimenti
 
    
    '''
    '''    self.d1(1) conrollo led verde blink veloce e dopo lento
        oppure led bianchi che possono essere leagti a selezione  comew per led biaNCHE SE 
        I LED BIANCHI SONO LEGAti a selettori D11 d12 ..d16 on on /OFF
    '''          
     
    def Marcia(self,occupa ,libera):
		self.Occupa(occupa)
		time.sleep(5)
		self.Libera(libera)
		time.sleep(5)
		self.D(1)
		
        
    ''' occupa ibera viene usato per occupare o liberare il cabale....'''
    ''' sono quattro  selettori che vengono usati per attivare il canale singolaermente'''
    '''' 1 puo essere On off'''
    '''  2 puo essere ON Off'''
    '''' 3 puo essere On off'''
    '''  4 puo essere ON Off'''
    ''' sono i selettori da d30 d32 d34 d36 per occupare '''
    ''' sono i selettori da d29 d31 d33 d35 per liberare'''
    ''' li devo attivare 1 a 1 '''
    
    def Testloop(self,numerodicicli=100):
        i=0
        Statuserror=0
        while(i<numerodicicli):
            time.sleep(1)
            if(self.tasti.Comando1(1)):
                print(" Numero di errori",Statuserror)
            else:
                Statuserror=Statuserror+1
                
            time.sleep(1)
            if(self.tasti.Comando1(0)):
                print(" Numero di errori",Statuserror)
            else:
                Statuserror=Statuserror+1
                
            print("onoff is",i)
            i=i+1
        return Statuserror
    '''
    questa funzione somma un errore in TX sul  frame che viene spedito
    può essere usata per la condizione di perdia link
    '''
    def AddRfTxError(self):
        pass
    '''
    questa funzione riceve un frame da BT e se attivo aggiunge un errore
    devo verificare se può essere usata per la condizione di perdita link
    '''
    def AddRfRxError(self):
        pass

    def checkFrameRx(self):
        pass
    def checkFrameTx(self):
        pass
    
    #questa funzione viene usata per  misurare il tempo di intervento dello stop
    #attenzione devo leggere gli stop di 4 riceventi o quidi fare la statistica.
    #PS.: so quando premo gli stop.... solo una misura di 4 pin...
    #ho la funzione di timer  e quindi leggo i tempi di attesa... gli passo la lista dei pin da leggere...
    #cosi il sistema è configurabile
    #quindi devo rilasciare gli stop sulla Tx e misurare il tempo di attesa
    
    def MisureAttivoStop(self,ListaCheckStopAttivo,timeout=100000, soglia=100):
        self.StopRilasciato()
        StatoStops=[]
        start = time.time()
        i=0
        while(i<len(ListaCheckStopAttivo)):
            GPIO.setup(ListaCheckStopAttivo[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            StatoStops.append(0)
            i=i+1
        k=0
        while(k<timeout):
            i=0
            while(i<len(ListaCheckStopAttivo)):
                if(GPIO.input(ListaCheckStopAttivo[i])==1):
                    StatoStops[i]=0 #in questo caso tutto ok
                else:
                    StatoStops[i]=StatoStops[i]+1 #condizione di allarme
                    if(StatoStops[i]>soglia):
                        end = time.time()
                        return(end-start)
                        
                i=i+1
            time.sleep(0.05)
            k=k+1
            end = time.time()
            print("timeout is",(end-start))
        return (end-start)
       
    
    #In questo caso tolgo alimentazione alla Trasmittente e/o da verificare aggiungo in errore nella nel BCH
    #ee quindi da quel punto in poi la TX mi da errore attenzione potrei decidere di ... aggiungere un certo numero di frame
    #errari. il parametro che passo ... numero consecutivo di frame errati.... 1,2,3,4,5,6,..255
    #La misura del tempo di intervento degli stop viene fatto come prima.
    
    def MisurepassivoStop(self,ListaCheckStopPassivo,timeout=100000,soglia=100):
        self.AlimTx=0
        StatoStops=[]
        start = time.time()
        i=0
        while(i<len(ListaCheckStopPassivo)):
            GPIO.setup(ListaCheckStopPassivo[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            StatoStops.append(0)
            i=i+1
        k=0
        while(k<timeout):
            i=0
            while(i<len(ListaCheckStopPassivo)):
                if(GPIO.input(ListaCheckStopPassivo[i])==1):
                    StatoStops[i]=0 #in questo caso tutto ok
                else:
                    StatoStops[i]=StatoStops[i]+1 #condizione di allarme
                    if(StatoStops[i]>soglia):
                        end = time.time()
                        return(end-start)
                        
                i=i+1
            time.sleep(0.05)
            k=k+1
            end = time.time()
            print("timeout is",(end-start))
        return (end-start)
        
    
    #spedisco un comando mi aspetto di leggere TX=Rx 
    #attenzione
    def MarciaTest(self,MarciaList=[],timeout=10000,soglia=100):
        
        StatoStops=[]
        start = time.time()
        i=0
        while(i<len(MarciaList)):
            GPIO.setup(MarciaList[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            StatoStops.append(0)
            i=i+1
        k=0
        while(k<timeout):
            i=0
            while(i<len(MarciaList)):
                if(GPIO.input(MarciaList[i])==1):
                    StatoStops[i]=0 #in questo caso tutto ok
                else:
                    StatoStops[i]=StatoStops[i]+1 #condizione di allarme
                    if(StatoStops[i]>soglia):
                        end = time.time()
                        return(end-start)
                        
                i=i+1
            time.sleep(0.05)
            k=k+1
            end = time.time()
            print("timeout is",(end-start))
        return (end-start)
       

######################################################
#Since I want to copy the whole disk, I execute:
#
#dd if=/dev/sdc of=sdimage.img bs=4M
#
#File sdimage.img, 7.9 GB (7,944,011,776 bytes) is created (SD card is 8 GB). Now I mount another SD card and execute:
#
#dd if=sdimage.img of=/dev/sdc bs=4M
#
######################################################

def  main():
    T=Tasti()
    T.CancellazioneMacAddress()

if __name__ == '__main__':
    main()
