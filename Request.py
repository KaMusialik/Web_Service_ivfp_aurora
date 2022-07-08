
import requests

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

# Schreiben in Response File
file = open("Response.xml", "wb")
file.write(response.content)

