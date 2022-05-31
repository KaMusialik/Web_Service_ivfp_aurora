# -*- coding: utf-8 -*-

from pathlib import Path
import os

class Protokoll:
    
    def __init__(self, f):
        self.file_protokoll = f
        datei= Path(self.file_protokoll)
        if datei.is_file():
            text="Datei " + self.file_protokoll+ " existiert."
            print(text)
            self.SchreibeInProtokoll(text)
            os.remove(self.file_protokoll)
            text='Datei ' + self.file_protokoll+ ' wird gelöscht.'
        else:
            print("Datei " + self.file_protokoll + " existiert nicht!!!")   
            datei.touch()
            print("Datei " + self.file_protokoll + " wurde angelegt!!!")   
        
    def DictionaryAusgeben(self, data_dict, itab=1):
        
        
        if itab == 0:
            itab = 1
            
        for name, wert in data_dict.items():
            
            if (type(wert) == list):
                #Wert is eine Liste
                text=str('\t'*itab) + str(name) + ': ' + str('')
                self.SchreibeInProtokoll(text)
                
                itab = itab + 1
                
                for einzelwert in wert:
                    self.DictionaryAusgeben(einzelwert, itab)
                    
                    
            else:
            
                text=str('\t'*itab) + str(name) + ': ' + str(wert)
                self.SchreibeInProtokoll(text)

            
    def SchreibeInProtokoll(self, text):
        print(text)
        text=text + "\n"
        f=open(self.file_protokoll, "a")
        f.write(text)    
        f.close()     