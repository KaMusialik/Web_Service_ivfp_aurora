# -*- coding: utf-8 -*-

from re import sub

class Parameter:
    
    def __init__(self, f):
        self.file = f

    def LeseParameter(self, name):
        datei=open(self.file, "r")
        
        ergebnis = {}
        for zeile in datei:
            ergebnis=self.ZerlegeZeileInNameWert(zeile)
            if ergebnis.get('name') == str(name):
                #Trefer:
                print('Ergebnis:', ergebnis)
                datei.close()
                return str(ergebnis.get('wert'))

        datei.close()
        return ''
        
    def ZerlegeZeileInNameWert(self,zeile):
        
        ergebnis={}
        
        if zeile[0] != '#':
            liste = zeile.split(':',1)
            name = str(liste[0])
            wert = str(liste[1])
            
            wert = sub('\n', '', wert)
            ergebnis['name'] = name
            ergebnis['wert'] = wert
            
        return ergebnis
                        