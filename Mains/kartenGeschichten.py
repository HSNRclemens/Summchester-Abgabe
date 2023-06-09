import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

#Dieses Skript hat bis zum Ende Probleme gemacht. Es sieht so aus, als würde durch die Bibliothek die reader.read()-Methode eine eigene schleife aufmachen, an die man nicht mehr dran kommt und das Programm macht dann soange nichts, bis der Reader was gefunden hat
#Der Code unten sollte eine 5-Sekundenschleife machen, die den Lesevorgang danach abbricht. Das hat aber alles nicht funktioniert. 
#Ich wollte in dem Projekt kein Multithreading benutzen (hätte ich wahrscheinlich auch nicht hinbekommen), deswegen gibt es jetzt eine Abbruchskarte, die 'None' zurückgibt. Damit kann man den Vorgang abbrechen, wenn man doch keine Karte vorhalten wollte.


def KarteLesen():
    global text
    try:
        startZeit = time.time()  
        print("Versuche Karte zu lesen")

        while True:
            if time.time() - startZeit >= 5:
                print("keine Karte gefunden...")
                break  

            id, text = reader.read()    #Das hier pausiert den Code an der Stelle, bis eine Karte gefunden wurde.
            if id is not None:
                break

            time.sleep(0.1)  
    finally:
        rtnText = text.replace(" ","")  #löscht alle Leerzeichen aus dem Text auf der Karte
        if(rtnText == "abort"): 
            print("Abbruchkarte")
            return None
        else: return rtnText




