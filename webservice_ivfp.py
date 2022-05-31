# -*- coding: utf-8 -*-

import requests
import protokoll as prot
import parameter as param
import json

class WebServiceIVFP:
    
    def __init__(self, f_dict):
        file_protokoll=f_dict.get('protokoll_file_AufrufWS_IVFP')
        self.oprot = prot.Protokoll(file_protokoll)

        file_parameter=f_dict.get('parameter_ivfp')
        self.oparam = param.Parameter(file_parameter)

        # setzt den Benutzername und das Passwort
        self.username = self.oparam.LeseParameter('username')
        print('ivfp:username', self.username)
        self.password = self.oparam.LeseParameter('password')
        print('ivfp:password:', self.password)

        # setzt die url, den header und die Post JSON
        self.url = self.oparam.LeseParameter('url')
        self.header = {'Content-type': 'application/json'}

        #hier werden die Daten für den Vertrag abgelegt, der aufgerufen werden soll        
        self.vertrag_dict = {}
        
        self.SetzteVertrag(f_dict.get('vertrag_dict'))

    def SetzteVertrag(self, vtg_dict):
        
        # spezifische für IVFP Angaben:
        self.vertrag_dict = {
            "aufrufnummer": 2,
            "test": True,
            "gesellschaftskennzeichen": "Pangaea Life",
            "tarif": "HR_SonderN",
            "fonds1": "IVFP80GARANT",
            "fonds2": "LU1675428244",
            "anteil_Fonds1": 1,
            "garantieniveau": 0.8,
            "mindesttodesfallleistung": 4,
            "prozentBtgSumme": 0,
        }
        
        # variable Angeben, die beim Aufruf vorgegebene werden:
        self.vertrag_dict['zahlbeitrag'] = vtg_dict.get('zahlbeitrag')
        self.vertrag_dict['zahlweise'] = vtg_dict.get('zahlweise')
        self.vertrag_dict['beitragszahlungsdauer'] = vtg_dict.get('beitragszahlungsdauer')
        self.vertrag_dict['versicherungsdauer'] = vtg_dict.get('versicherungsdauer')
        self.vertrag_dict['versicherungsbeginn'] = vtg_dict.get('versicherungsbeginn')
        self.vertrag_dict['geburtsdatum'] = vtg_dict.get('geburtsdatum')
        
        self.oprot.SchreibeInProtokoll('------------- Anfang:')
        self.oprot.SchreibeInProtokoll('Input Vertrag IVFP:')
        self.oprot.SchreibeInProtokoll(str(self.vertrag_dict))
        self.oprot.DictionaryAusgeben(self.vertrag_dict)
        self.oprot.SchreibeInProtokoll('------------- Ende')
        print('Input Vertrag IVFP:')
        
    
    #  function, fuer eine verschoenerte darstellung
    def print_output(self, header, content):
        print(header)
        print(content)
        for x in range(20):
            print("-", end="")
        print()

    def aufrufWebservice(self):

        # macht ein post request, mit der url, der authentification, den header und die json die geposted werden soll
        response = requests.post(self.url, auth=(self.username, self.password), headers=self.header, json=self.vertrag_dict)
        
        print()
        
        # gibt den response in der konsole aus
        self.print_output('Response Code', response)
        self.print_output('Response Header', response.headers)
        self.print_output('Response', response.text)
        
        return response.text
    
    def LeseNameUndWert(self, name):
        ausgang={}
        str_name = str(name)
        laenge = len(str_name)
        position = str_name.find('_')
        if position == -1:
            position = laenge
            
        text_vor_position = str_name[0:position]
        text_nach_position = str_name[position+1:]
        ausgang['name_text1'] = text_vor_position
        ausgang['name_text2'] = text_nach_position
        return ausgang
        
    def LeseAblaufleistung(self, outputDaten):
        dict_alles = {}
        dict_ablaufleistung = {}
        dict_name_wert = {}
        
        dict_alles = outputDaten
        
        if dict_alles.get('ablaufleistungen') == None:
            
            # Das Feld aböaufleistungen ist nicht gefüllt
            for name, wert in dict_alles.items():
                if name == 'minimum':
                    dict_ablaufleistung[0] = wert
                    pass
                elif name == 'maximum':
                    dict_ablaufleistung[1000] = wert
                    pass
                else:
                    dict_name_wert=self.LeseNameUndWert(name)
                    if dict_name_wert['name_text1']=='ablauf':
                        nummer = int(dict_name_wert.get('name_text2'))
                        dict_ablaufleistung[nummer] = wert
                    
        else:
            ablaufleistungen = []
            ablaufleistungen = dict_alles.get('ablaufleistungen')
            
            nummer = 0
            for wert in ablaufleistungen:
                dict_ablaufleistung[nummer] = wert
                nummer += 1
        
        print('------------- Anfang:')
        print('Ablaufleistung:')
        print(dict_ablaufleistung)
        print('------------- Ende')
        
        return dict_ablaufleistung
        
    def LeseOutput(self, respose_str):
        
        dict1 = {}
        dict1 = json.loads(respose_str)
    
        print('------------- Anfang:')
        print('Response Output:')
        print(dict1)
        print('------------- Ende')


        return dict1
