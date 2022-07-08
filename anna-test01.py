# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import xml.etree.ElementTree as et
import pandas as pd

# Request machen:
# Statische URL zum Webservice Aurora
url = 'https://aurorapreview.ivfp.de/api/values'
headers = {"Content-Type":"application/xml; charset=utf-8"}

# Einlesen des XML-Files
xml_file_name = input("Bitte geben Sie den Namen der Datei des Requests an: ")

xml_file = open(xml_file_name, "rb")
xml_inhalt = xml_file.read()
xml_file.close

# Abschicken des Requests
response = requests.post(url, data=xml_inhalt, headers=headers)

# Schreiben in Response File (funktioniert noch nicht so gut)
file = open("Response.xml", "wb")
file.write(response.content)
# Alternative von Anna:
root = et.fromstring(response.text)
tree = et.ElementTree(root)
tree.write("Responsefile.xml")

xtree = et.parse('Responsefile.xml')
root = tree.getroot()

