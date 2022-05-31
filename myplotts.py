#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import protokoll as prot


class MyPlotts:
    def __init__(self, f_dict):
        file_protokoll=f_dict.get('protokoll_file_MyPlotts')
        self.oprot = prot.Protokoll(file_protokoll)

    def WeitereParameter(self, f_grafik_file):
        self.grafik_file = f_grafik_file

    def PlotteAblaufleistung(self, data_dict_ivfp, data_dict_mum):
        
        text = '------------- Beginn myplotts/PlotteAblaufleistung:'
        self.oprot.SchreibeInProtokoll(text)

        #Eingangsdaten von IVFP werden protokolliert:
        text = '------------- Beginn myplotts/data_dict_ivfp:'
        self.oprot.SchreibeInProtokoll(text)
        text = 'data_dict_ivfp: ' + str(data_dict_ivfp)
        self.oprot.SchreibeInProtokoll(text)
        
        self.oprot.DictionaryAusgeben(data_dict_ivfp)

        text = '------------- Ende myplotts/data_dict_ivfp'
        self.oprot.SchreibeInProtokoll(text)

        #Eingangsdaten von MuM werden protokolliert:
        text = '------------- Beginn myplotts/data_dict_mum:'
        self.oprot.SchreibeInProtokoll(text)
        text = 'data_dict_mum: ' + str(data_dict_mum)
        self.oprot.SchreibeInProtokoll(text)
        
        self.oprot.DictionaryAusgeben(data_dict_mum)

        text = '------------- Ende myplotts/data_dict_mum'
        self.oprot.SchreibeInProtokoll(text)

        
        
        fig1, ax1 = plt.subplots()
        
        data_ivfp = []
        data_mum = []
        for nummer, wert in data_dict_ivfp.items():
            data_ivfp.insert(nummer, float(wert))

        for nummer, wert in data_dict_mum.items():
            data_mum.insert(int(nummer), float(wert))
            

        box_plot_data=[data_ivfp,data_mum]

        ax1.set_title('Ablaufleistung')
        
        ax1.boxplot(box_plot_data, vert=False, sym='', labels=['IVFP', 'MuM'], patch_artist=True)

        plt.savefig(self.grafik_file)
        text = '------------- Ende myplotts/PlotteAblaufleistung'
        self.oprot.SchreibeInProtokoll(text)
