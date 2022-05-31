# -*- coding: utf-8 -
from fpdf import FPDF
import pandas as pd

class PDF(FPDF):
    def __init__(self, pdf_init_dict):
        super().__init__()
        self.titel = pdf_init_dict.get('Titel')
        self.margin = pdf_init_dict.get('Margin')
        self.fonds_style = pdf_init_dict.get('Fonds_Style')

    def header(self):
        self.set_font(self.fonds_style, 'B', self.margin)
        self.cell(0, 10, self.titel, border=True, ln=True, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.fonds_style, 'I', 10)
        self.cell(0, 10, f'Seite {self.page_no()}/{{nb}}', align='C' )

class MyPDF:
    
    def __init__(self, f_pdf, f_text):
        self.filePDF = f_pdf
        self.fileText = f_text
        self.margin = 0
        self.InitialisiereWerte()

    def InitialisiereWerte(self):
        wert_dict = {}
        wert_dict['nummer'] = str(0)
        wert_dict['name'] = str('Margin')
        self.LeseAusText(wert_dict)
        self.margin = int(wert_dict.get('wert'))

        wert_dict['name'] = str('Titel')
        self.LeseAusText(wert_dict)
        self.titel = wert_dict.get('wert')

        wert_dict['name'] = str('Fonds_Style')
        self.LeseAusText(wert_dict)
        self.Fonds_Style = wert_dict.get('wert')

    def AnzahlDerKapitel(self):
        df = pd.read_csv(self.fileText, sep=";", dtype=object)
        anzahl = int(df['nummer'].max())

        return anzahl

    def LeseAusText(self, wert_dict):
        nummer = wert_dict.get('nummer')
        name = wert_dict.get('name')

        df = pd.read_csv(self.fileText, sep=";", dtype=object)
        df1 = df[(df.nummer == nummer) & (df.name == name)]

        if df1.__len__() != 1:
            wert_dict['wert'] = None
        else:
            index = df1.index[0]
            wert = str(df1.at[index, 'wert'])
            wert = wert.lstrip()
            wert = wert.strip()
            wert_dict['wert'] = wert

    def SchreibePDF(self):
        pdf_init_dict = {}
        pdf_init_dict['Margin'] = self.margin
        pdf_init_dict['Titel'] = self.titel
        pdf_init_dict['Fonds_Style'] = self.Fonds_Style

        pdf = PDF(pdf_init_dict)

        pdf.set_auto_page_break(auto=True, margin=self.margin)

        wert_dict = {}
        text_dict = {}

        pdf.add_page()

        for i in range(1,  self.AnzahlDerKapitel()+1):
            wert_dict['nummer'] = str(i)

            wert_dict['name'] = str('Ueberschrift')
            self.LeseAusText(wert_dict)
            text_dict['Ueberschrift'] = wert_dict.get('wert')

            wert_dict['name'] = str('Fonds_Size_Ueberschrift')
            self.LeseAusText(wert_dict)
            text_dict['Fonds_Size_Ueberschrift'] = str(wert_dict.get('wert'))

            wert_dict['name'] = str('Fonds_Size_Text')
            self.LeseAusText(wert_dict)
            text_dict['Fonds_Size_Text'] = str(wert_dict.get('wert'))

            wert_dict['name'] = str('Fonds_Style')
            self.LeseAusText(wert_dict)
            text_dict['Fonds_Style'] = wert_dict.get('wert')

            wert_dict['name'] = str('Text')
            self.LeseAusText(wert_dict)
            text_dict['Text'] = wert_dict.get('wert')

            style = text_dict.get('Fonds_Style')
            size = int(text_dict.get('Fonds_Size_Ueberschrift'))
            pdf.set_font(family=style, size=size)
            pdf.cell(0, 10, text_dict.get('Ueberschrift'), ln=True)

            size = int(text_dict.get('Fonds_Size_Text'))
            pdf.set_font(family=style, size=size)
            pdf.multi_cell(180, 5, text_dict.get('Text'))

        pdf.alias_nb_pages()
        pdf.output(self.filePDF)