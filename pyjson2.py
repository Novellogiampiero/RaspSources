import json
import plotfi
import os, fnmatch
from os import listdir
from os.path import isfile, join
try:
    import matplotlib.pyplot as plt
    import matplotlib.widgets as widgets
    import numpy as np
    from scipy.signal import butter,filtfilt
except:
    print("Sono in raspberry")
def TestParameterWr(filename,NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,Dati=[]):
    TestGuiliano = {
                    "NomeTest":None,
                    "data":None,
                    "Articolo":None,
                    "NodoRasp":None,
                    "DescrizioneIngresso": None,
                    "BitQuantiz":None,
                    "NumeroCiclo":None,
                    "BandaFiltro" :None,
                    "FrequenzadiCampionamento":None,
                    "NumeroCampioni": None,
                    "ERRORI":None,
                    "Dati": []
                    }
    Dati_dict = json.dumps(TestGuiliano)
    #print(type(Dati_dict))
    Testdata= json.loads(Dati_dict)
    #print(type(Testdata))
    #print(Testdata)
    Testdata["NomeTest"]=NomeTest
    Testdata["data"]=data
    Testdata["Articolo"]=Articolo
    Testdata["NodoRasp"]=Nodo
    Testdata["DescrizioneIngresso"]=DescrizIngresso
    Testdata["BitQuantiz"]=BitQuant
    Testdata["NumeroCiclo"]=NumeroCiclo
    Testdata["BandaFiltro"]=Banda
    Testdata["FrequenzadiCampionamento"]=Fc
    Testdata["NumeroCampioni"]=NumeroCampioni
    Testdata["ERRORI"]=Errori
    i=0
    while(i<len(Dati)):
        Testdata["Dati"].append(Dati[i])
        i=i+1
    #Testdata["Dati"].append(Dati[0])
    #Testdata[Dati].append(Dati[0])
    #print(Testdata)
    with open(filename, 'w') as filejson:
        json.dump(Testdata, filejson)
        filejson.close()

def TestParameterRdForDB(filename):
    with open(filename) as jsonFile:
        Testdata = json.load(jsonFile)
        jsonFile.close()
    print(" data is ",Testdata)
    return json.dumps(Testdata)
   
def TestParameterRd(filename):
    with open(filename) as jsonFile:
        Testdata = json.load(jsonFile)
        jsonFile.close()
    print(" data is ",Testdata)
    #return json.dumps(Testdata)
    NomeTest=Testdata["NomeTest"]
    data=Testdata["data"]
    Articolo=Testdata["Articolo"]
    Nodo=Testdata["NodoRasp"]
    DescrizIngresso=Testdata["DescrizioneIngresso"]
    BitQuant=Testdata["BitQuantiz"]
    NumeroCiclo=Testdata["NumeroCiclo"]
    Banda=Testdata["BandaFiltro"]
    Fc=Testdata["FrequenzadiCampionamento"]
    NumeroCampioni=Testdata["NumeroCampioni"]
    Errori=Testdata["ERRORI"]
    #Dati=Testdata["Dati"]
    return NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori

def TestRd(filename):
    with open(filename) as jsonFile:
        Testdata = json.load(jsonFile)
        jsonFile.close()
    print(" data is ",Testdata)
    #return json.dumps(Testdata)
    NomeTest=Testdata["NomeTest"]
    data=Testdata["data"]
    Articolo=Testdata["Articolo"]
    Nodo=Testdata["NodoRasp"]
    DescrizIngresso=Testdata["DescrizioneIngresso"]
    BitQuant=Testdata["BitQuantiz"]
    NumeroCiclo=Testdata["NumeroCiclo"]
    Banda=Testdata["BandaFiltro"]
    Fc=Testdata["FrequenzadiCampionamento"]
    NumeroCampioni=Testdata["NumeroCampioni"]
    Errori=Testdata["ERRORI"]
    Dati=Testdata["Dati"]
    return NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,Dati

''' questa funzione viene usata per plottare tutti i jsonfile'''

def PlotJsonFile(filenameMask):
    fileMask=filenameMask+"*"+".json"
    fils=plotfi.findfile(fileMask,'.')
    NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,Dati=TestRd(fils)
    plt.plot(Dati)
    plt.show()
    
''' leggo ilconfiguration file formato json'''
def ReadConfig(filename):
    with open(filename) as jsonFile:
        Testdata = json.load(jsonFile)
        jsonFile.close()
    print(" data is ",Testdata)
    NomeTest=Testdata["NomeTest"]
    NumeroTot=Testdata["NumeroTotale"]
    NumeroParziale=Testdata["Save"]
    Nodo=Testdata["Nodo"]
    return NomeTest,NumeroTot,NumeroParziale,Nodo
    
''' scrivo il file di configuraione json'''

def WriteConfig(filename,NumeroTot=1000000,SiSalvaOgni=1000,NomeTest="test1",Nodo="NomedellaRaspberry"):
    Config = {
                "NomeTest":None,
                "NumeroTotale":None,
                "Save":None,
                "Nodo": None
            }
    Dati_dict = json.dumps(Config)
    Testdata= json.loads(Dati_dict)
    Testdata["NomeTest"]=NomeTest
    Testdata["NumeroTotale"]=NumeroTot
    Testdata["Save"]=SiSalvaOgni
    Testdata["Nodo"]=Nodo
    i=0
    print(Testdata)
    with open(filename, 'w') as filejson:
        json.dump(Testdata, filejson)
        filejson.close()
    
def main():
    WriteConfig("ttt.json",NumeroTot=1000,SiSalvaOgni=10,NomeTest="T1",Nodo="NomedellaRaspberry")
    print("TX",ReadConfig("ttt.json"))
    return
    fils=plotfi.findfile('demo*.txt','.')
    print("fils isi ====>>>>",fils)
    i=0
    while(i<len(fils)):
        A=plotfi.readfile(fils[i])
        fileis=fils[i]+".json"
        #TestParameterWr(filename=fileis,NomeTest="Test",data="10.3.2021",Articolo="mio",Nodo="rasp1",DescrizIngresso="ingresso0",BitQuant="8",NumeroCiclo="100",Banda="16k",Fc=16000,NumeroCampioni=24000,Errori="OK",Dati=A)
        print(TestParameterRd(filename))
        i=i+1


if __name__ == "__main__":
    main()
