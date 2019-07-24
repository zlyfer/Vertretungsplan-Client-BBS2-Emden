import json
import requests
print ("available parameter: Kurs, Stunde, Fach, Raum, Lehrer, Info, Vertretungstext, Datum, kurs, stunde, fach, raum, lehrer, info, vertretungstext, datum")
print ("parameter example: Kurs=BG-13 > searches for BG-13")
print ("parameter example: kurs=false > disables kurs")
print ("use %20 for space")
link = "https://zlyfer.de/vertretungsplan/api/api.php?interface=false"
postfix = False
while postfix != "":
    postfix = input("parameter (leave blank to continue): ")
    if postfix != "":
        link += "&" + postfix
session = requests.session()
response = session.get(link).text
json = json.loads(response)
count = len(json['vertretungen'])
print("\n")
print("Using link: %s" % link)
print ("%s entries found." % count)
input("Press any key to display fetch.")
for i in range(count):
    entry = json['vertretungen'][i]
    print ("\n%s:" % str(i+1))
    for k in entry:
        print ("    %s: %s" % (k, entry[k]))
input()
