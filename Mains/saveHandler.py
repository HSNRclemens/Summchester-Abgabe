import os
current_dir = os.path.dirname(os.path.abspath(__file__))

#Hier können die wichtigen Variablen eines Liedes auf dem Gerät gespeichert werden um sie später wieder aufrufen zu können.
#Ich baue die Werte in eine Textdatei ein und trenne die Abschnitte mit Sonderzeichen. 
#Die erste Methode habe ich dann an ChatGPT geschickt, kurz erklärt worum es geht und darum gebeten, die Methode rückwärts zu schreiben und zu kommentieren. Für sowas kann das echt praktisch sein.

#Die Methode zum Speichern
def saveAs(name, inhalt, speed,taktAnz):

    #erstmal rechnen wir den Inhalt in einen String um, der wird dann als Lied.irk gespeichert.
    content = str(speed)+"$"+str(taktAnz) +"$"
    for i in range(len(inhalt)):
        content += "~"
        for j in inhalt[i]:
            content +="|"+str(j)

    pfad = os.path.join(current_dir, 'Lieder', (str(name) + ".irk"))

    with open(pfad,"w") as dokument:
        dokument.write(content)

#Das ist von ChatGPT geschrieben und kommentiert
def openFrom(name):
    # Konstruiere den Dateipfad basierend auf dem aktuellen Verzeichnis, dem Unterverzeichnis "Lieder" und dem Dateinamen mit der Erweiterung ".irk"
    pfad = os.path.join(current_dir, 'Lieder', (str(name) + ".irk"))

    try:
        # Öffne die Datei im Lese-Modus
        with open(pfad, "r") as dokument:
            # Lese den gesamten Inhalt der Datei
            content = dokument.read()

        # Teile den Inhalt in Abschnitte auf, die durch das Tilde-Zeichen "~" getrennt sind
        sections = content.split("~")

        # Extrahiere die Geschwindigkeit und die Taktanzahl aus dem ersten Abschnitt
        # Trenne den Abschnitt am Dollar-Zeichen "$" auf und weise den ersten Teil der Geschwindigkeit zu und den zweiten Teil der Taktanzahl
        speed = int(sections[0].split("$")[0])
        taktAnz = int(sections[0].split("$")[1])

        # Initialisiere eine leere Liste für den Inhalt
        inhalt = []

        # Iteriere über die restlichen Abschnitte und konvertiere die Werte in Arrays
        for section in sections[1:]:
            # Trenne den Abschnitt am senkrechten Strich "|" auf und konvertiere die substrings zu Integer-Werten
            array = [int(x) for x in section.split("|")[1:]]
            # Füge das Array zur Inhalt-Liste hinzu
            inhalt.append(array)

        # Gib die extrahierten Werte speed, taktAnz und inhalt als Tuple zurück
        return speed, inhalt, taktAnz

    except (IOError, ValueError, IndexError):
        # Falls ein Fehler beim Lesen oder Analysieren der Datei auftritt, gib None, None, None zurück
        return None, None, None



"""
-----------------------------------------------------------------------------------------
Ich kann die Dateien der Lieder nicht kommentieren, deswegen hier kurz etwas dazu:

Ein Lied könnte zum Beispiel so aussehen:
500$4$~|21|-1|21|-1|-1|21|20|-1~|16|-1|17|-1|-1|16|17|-1~|11|10|12|10|11|10|12|10~|4|-1|4|-1|4|3|2|1~|4|-1|4|-1|4|3|2|1~|-1|-1|-1|-1|-1|-1|-1|-1~|24|-1|-1|-1|-1|24|-1|24~|-1|-1|-1|-1|-1|-1|-1|-1

Die erste 500 steht dafür, dass ein Ton in dem Lied 500 ms dauert, danach kommt das Trennzeichen $
die 4 steht dafür, dass der Taktservo alle 4 Takte ausschlägt, dann folgt das Trennzeichen $
mit dem ~ beginnt der eigentliche Inhalt des Lieds, durch '|' getrennt werden jetzt die Töne für jeweils die 8 Farben aufgeschrieben. -1 heißt kein Ton und '~' bedeutet, das hier ein neuer Farbbereich anfängt.
-----------------------------------------------------------------------------------------
"""