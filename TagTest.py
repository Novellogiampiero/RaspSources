import NfcLibCriptedI2c
import TastiRpiNew
import iicTodo
import time
#queste 3 librerie realizzano tutte le interfacce possibili.
def Setup1():
    Tasti=TastiRPi()
    Tasti.SetAlimTag(0)
    Tasti.SetTastoTag(0)
    Tasti.ReleI2C(0) # mi  preparo alla scrittura del TAG
    time.sleep(10)
    RR=NfcLibCriptedI2c.SetTagData(sicurezza=7,KeyType=0x09,Azione=8,Cripted=True)
    print("Len RR is ",len(RR)
    I2CWrite(RR) # scrivo il tag 
    NfcLibCriptedI2c.I2CRead() #leggo il tag 
    Tasti.SetAlimTag(1)
    Tasti.SetTastoTag(0)  #lo disalimento .. resettandolo
    time.sleep(10)
    Tasti.Accensione()   # alimento il reader
    i=0
    Tasti.ReleI2C(1)    #alibito I2C del reader.
    time.sleep(2)
    Tasti.SetAlimTag(1)
    Tasti.SetTastoTag(0)
    time.sleep(60)
    #LEGGO i2c
    Res0=i2cAddess(data,action=2,iaddr=0x00,iaddr_bytes = 2,datasize=32,loop=1)
    ResC00=i2cAddess(data,action=2,iaddr=0x0c00,iaddr_bytes = 2,datasize=32,loop=1)
    ResC20=i2cAddess(data,action=2,iaddr=0x0c00,iaddr_bytes = 2,datasize=32,loop=1)
    Tmp.Spegnimento()
