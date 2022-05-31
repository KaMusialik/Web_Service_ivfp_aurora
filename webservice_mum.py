# -*- coding: utf-8 -*-

import requests
import json
import protokoll as prot
import parameter as param
import random

class WebServiceMuM:
    
    def __init__(self, f_dict):
        file_protokoll=f_dict.get('protokoll_file_AufrufWS_MUM')
        self.oprot = prot.Protokoll(file_protokoll)

        file_parameter=f_dict.get('parameter_mum')
        self.oparam = param.Parameter(file_parameter)
        
        # setzt den Benutzername und das Passwort
        self.username = self.oparam.LeseParameter('username')
        print('mum:username: ', self.username)
        self.password = self.oparam.LeseParameter('password')
        print('mum:password: ', self.password)
        self.token = ''

        # setzt die url, den header
        self.url_volatium = self.oparam.LeseParameter('url_volatium')
        self.url_login = self.oparam.LeseParameter('url_login')
        self.header = {}

        self.LeseToken()        

        #hier werden die Daten für den Vertrag abgelegt, der aufgerufen werden soll        
        self.vertrag_dict = {}
        
        self.SetzteVertrag(f_dict.get('vertrag_dict'))

    def LeseToken(self):
        data={'username': self.username, 'password': self.password}
        r= requests.post(self.url_login, json=data)

        text = '------------- Beginn LeseToken:'
        self.oprot.SchreibeInProtokoll(text)
        
        text = 'r.status_code:' + str(r.status_code)
        self.oprot.SchreibeInProtokoll(text)
        
        text = 'r.headers:' + str(r.headers)
        self.oprot.SchreibeInProtokoll(text)

        text = 'r.encoding:' + str(r.encoding)
        self.oprot.SchreibeInProtokoll(text)

        text = 'r.text:' + str(r.text)
        self.oprot.SchreibeInProtokoll(text)

        text = 'r.url:' + str(r.url)
        self.oprot.SchreibeInProtokoll(text)

        text = 'r.content:' + str(r.content)
        self.oprot.SchreibeInProtokoll(text)

        text_dict = {}
        text_dict = json.loads(r.text)

        text = 'text_dict:' + str(text_dict)
        self.oprot.SchreibeInProtokoll(text)
        self.token = text_dict.get('token')

        text = 'token: ' + str(self.token)
        self.oprot.SchreibeInProtokoll(text)

        text = '------------- Ende LeseToken'
        self.oprot.SchreibeInProtokoll(text)

    def SetzteVertrag(self, vtg_dict):
        
        # spezifische für IVFP Angaben:
        self.vertrag_dict = {
            "nichtraucherstatus": "Nichtraucher10Jahre",
            "hoehstmoeglichebeitragsgarantie": False,
            "beitragsgarantie": 0.0,
            "todesfallleistungAufschubzeit": "MaxBeitragsrueckgewaehrGuthaben",
            "prozentBtgSumme": 0,
            "fonds": "DE0009848119",
            "wertsicherungsfonds": "",
            "tarifId": 41533,
            "strategieId": 0,
            "ueberschusssystem": "Fondsueberschuesse",
            "hoechstmoeglicheBeitragsgarantie": True,
            "mindesttodesfallschutzWert": 0.0,
            "rentengarantiezeit": 5,
            "kapitalrueckgewaehr": False,
            "rentenbezugsform": "Dynamisch",
            "mitAblaufleistung": True,
            "beitragsdynamik": 0.0,
            "bAVTarife": "BZML"
            }

        
        # variable Angeben, die beim Aufruf vorgegebene werden:
        self.vertrag_dict['beitrag'] = vtg_dict.get('zahlbeitrag')
        if vtg_dict.get('zahlweise') == 12:
            self.vertrag_dict['zahlweise'] = 'Monatlich'
        else:
            self.vertrag_dict['zahlweise'] = 'Einmalbeitrag'
            
        self.vertrag_dict['beitragszahlungsdauer'] = vtg_dict.get('beitragszahlungsdauer')
        self.vertrag_dict['aufschubzeit'] = vtg_dict.get('versicherungsdauer')
        self.vertrag_dict['versicherungsbeginn'] = vtg_dict.get('versicherungsbeginn')
        self.vertrag_dict['geburtsdatum'] = vtg_dict.get('geburtsdatum')
        
        self.oprot.SchreibeInProtokoll('------------- Anfang:')
        self.oprot.SchreibeInProtokoll('Input Vertrag MuM:')
        self.oprot.SchreibeInProtokoll(str(self.vertrag_dict))
        self.oprot.DictionaryAusgeben(self.vertrag_dict)
        self.oprot.SchreibeInProtokoll('------------- Ende')
        print('Input Vertrag MuM:')
        
    

    def aufrufWebservice(self):

        text = '------------- BEGINN aufrufWebserviceMuM:'
        print(text)
        self.oprot.SchreibeInProtokoll(text)

        #setzte den Header:
        self.header['accept']= 'text/plain'
        self.header['Authorization']= 'Bearer ' + self.token
        self.header['Content-Type']= 'application/json-patch+json'
        
        text = 'gesetzter header:' +str(self.header)
        print(text)
        self.oprot.SchreibeInProtokoll(text)
        

        # macht ein post request, mit der url, der authentification, den header und die json die geposted werden soll
        r = requests.post(self.url_volatium, headers=self.header, json=self.vertrag_dict)

        text = 'r.status_code:' + str(r.status_code)
        self.oprot.SchreibeInProtokoll(text)
        
        text = 'r.headers:' + str(r.headers)
        self.oprot.SchreibeInProtokoll(text)

        text = 'r.encoding:' + str(r.encoding)
        self.oprot.SchreibeInProtokoll(text)

        text = 'r.text:' + str(r.text)
        self.oprot.SchreibeInProtokoll(text)

        text = 'r.url:' + str(r.url)
        self.oprot.SchreibeInProtokoll(text)

        text = 'r.content:' + str(r.content)
        self.oprot.SchreibeInProtokoll(text)


        text = '------------- ENDE aufrufWebserviceMuM'
        self.oprot.SchreibeInProtokoll(text)

        return r.text
        
    def LeseOutput(self, respose_str):
        
        dict1={}
        
        text = '------------- BEGINN MuM/LeseOutput:'
        self.oprot.SchreibeInProtokoll(text)

        text = 'Eingangstext: ' + respose_str
        self.oprot.SchreibeInProtokoll(text)

        text = ''
        self.oprot.SchreibeInProtokoll(text)

        dict1=json.loads(respose_str)

        text = 'Umwandlung in Dict: ' + str(dict1)
        self.oprot.SchreibeInProtokoll(text)

        self.oprot.DictionaryAusgeben(dict1)

        text = '------------- ENDE MuM/LeseOutput'
        self.oprot.SchreibeInProtokoll(text)


        return dict1
    
    def LeseAblaufleistung(self, outputDaten):
        dict_ablaufleistung = {}
        
        for i in range(0,1000):
            wert=random.randint(20000,200000)
            dict_ablaufleistung[str(i)]=wert
            
        text = '------------- Anfang MuM/LeseAblaufleistung:'
        self.oprot.SchreibeInProtokoll(text)

        text = '------------- Anfang AblaufleistungMuM:'
        self.oprot.SchreibeInProtokoll(text)
        self.oprot.SchreibeInProtokoll(str(dict_ablaufleistung))
        self.oprot.DictionaryAusgeben(dict_ablaufleistung)

        text = '------------- ENDE AblaufleistungMuM:'
        self.oprot.SchreibeInProtokoll(text)
        
        
        text = '------------- Ende MuM/LeseAblaufleistung'
        self.oprot.SchreibeInProtokoll(text)
        
        return dict_ablaufleistung    
