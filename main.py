# -*- coding: utf-8 -*-

#import sys
#import PyQt5.QtCore as core
#import PyQt5.QtWidgets as widgets
#import PyQt5.QtGui as gui
#import PyQt5.uic as uic

import protokoll as prot
import webservice_ivfp as ws_ivfp
import webservice_mum as ws_mum
import myplotts as myplt
import mypdf as mypdf

inputDaten={}

outputDaten_ivfp={}
outputDaten_mum={}

ablaufleistung_ivfp={}
ablaufleistung_mum={}

files_dict={}

#Vertrag:
vertrag_dict={}    
    
#work directory:
#fuer Linux:
files_dict['work_dir']='/home/karol/PycharmProjects/WebService/'
#fuer Apple:
#files_dict['work_dir']='/Users/karol/MeineProjekte/WebService/WEbservice/'

#einzelne Dateien:
files_dict['mainwindow_file']=files_dict.get('work_dir')+'mainWindow.ui'
files_dict['input_output_file']=files_dict.get('work_dir')+'input_output_file.txt'
files_dict['protokoll_file_main']=files_dict.get('work_dir')+'protokoll_main.txt'
files_dict['protokoll_file_InputOutput']=files_dict.get('work_dir')+'protokoll_InputOutput.txt'
files_dict['protokoll_file_AufrufWS_IVFP']=files_dict.get('work_dir')+'protokoll_AufrufWS_IVFP.txt'
files_dict['protokoll_file_AufrufWS_MUM']=files_dict.get('work_dir')+'protokoll_AufrufWS_MUM.txt'
files_dict['parameter_mum']=files_dict.get('work_dir')+'parameter_mum.txt'
files_dict['parameter_ivfp']=files_dict.get('work_dir')+'parameter_ivfp.txt'
files_dict['protokoll_file_MyPlotts'] = files_dict.get('work_dir')+'protokoll_MyPlotts.txt'
files_dict['grafik_file_MyPlotts'] = files_dict.get('work_dir')+'grafik_file.png'
files_dict['pdf_file_ivfp']=files_dict.get('work_dir')+'pdf_ivfp.pdf'
files_dict['pdf_text_file_ivfp']=files_dict.get('work_dir')+'pdf_text_ivfp.txt'


#spezifische Vertragsangaben für den Vertrag, der gerechnet werden soll:
vertrag_dict = {"zahlbeitrag": 100,
    "zahlweise": 12,
    "beitragszahlungsdauer": 37,
    "versicherungsdauer": 37,
    "versicherungsbeginn": "2022-04-01",
    "geburtsdatum": "1992-01-01T00:00:00"
}

files_dict['vertrag_dict'] = vertrag_dict

#app = widgets.QApplication(sys.argv)

#wMainwindow=uic.loadUi(files_dict.get('mainwindow_file'))    

print('****** Beginn der Berechnung *******')

oprot = prot.Protokoll(files_dict.get('protokoll_file_main'))

# Initialisierung der Webservices:
ows_ivfp = ws_ivfp.WebServiceIVFP(files_dict)
ows_mum = ws_mum.WebServiceMuM(files_dict)

#Aufruf der WebServices:
response_str_ivfp=str(ows_ivfp.aufrufWebservice())
response_str_mum=str(ows_mum.aufrufWebservice())

outputDaten_ivfp = ows_ivfp.LeseOutput(response_str_ivfp)
outputDaten_mum = ows_mum.LeseOutput(response_str_mum)

ablaufleistung_ivfp=ows_ivfp.LeseAblaufleistung(outputDaten_ivfp)
ablaufleistung_mum=ows_mum.LeseAblaufleistung(outputDaten_mum)

omyplt = myplt.MyPlotts(files_dict)
omyplt.WeitereParameter(files_dict.get('grafik_file_MyPlotts'))
omyplt.PlotteAblaufleistung(ablaufleistung_ivfp, ablaufleistung_mum)    

omypdf = mypdf.MyPDF(files_dict.get('pdf_file_ivfp'), files_dict.get('pdf_text_file_ivfp'))
omypdf.SchreibePDF()

print('****** Ende der Berechnung *******')

#wMainwindow.show()
#sys.exit(app.exec_())