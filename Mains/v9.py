import pygame
import os
import math

#selbstgebaute Skripte, damit der Code halbwegs übersichtlich bleibt...
import konstanten
import tonoutsource
import saveHandler
import kartenGeschichten
import servo

version = "1.9"

#Pygame-bibliothek starten
pygame.init()

#GUI Elemente
current_dir = os.path.dirname(os.path.abspath(__file__))
sprite_Spalte = pygame.image.load(os.path.join(current_dir,'..','Design', 'Gui', 'Spalte.png'))
sprite_Noten = pygame.image.load(os.path.join(current_dir, '..', 'Design', 'Gui', 'Noten.png'))
sprite_Plus = pygame.image.load(os.path.join(current_dir, '..', 'Design', 'Gui', 'PlusKnopp.png'))
sprite_Minus = pygame.image.load(os.path.join(current_dir, '..', 'Design', 'Gui', 'MinusKnopp.png'))
sprite_Punkt = pygame.image.load(os.path.join(current_dir, '..', 'Design', 'Gui', 'Punkt.png'))
sprite_Pause = pygame.image.load(os.path.join(current_dir, '..', 'Design', 'Gui', 'Pause.png'))

#statischeKnoppe holen
#Die Knöpfe für Kopfzeile, also Stop-, Start- und Pauseknopf
knop_kopf = []
for e in konstanten.stButtons[0]:
    knop_kopf.append(pygame.image.load(os.path.join(current_dir,'..','Design', 'Gui', e[1])))

#Knöpfe für Kopfzeile4
knop_kopf4 = []
for e in konstanten.stButtons[2]:
    knop_kopf4.append(pygame.image.load(os.path.join(current_dir,'..','Design', 'Gui', e[1])))

#Knöpfe für die Navigationsleiste unten
knop_nav = []
for e in konstanten.stButtons[1]:
    knop_nav.append(pygame.image.load(os.path.join(current_dir,'..','Design', 'Gui', e[1])))

#Fonts holen
font_small = pygame.font.Font(None,32)
font_big = pygame.font.Font(None,66)



#Hauptvariablen
anzSpalten = 1;                                             #Wie viele Spalten gint es? (mindestens 1, bis theoretisch unbegrenzt)
tonhalter = [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]]       #Das Herzstück des Programms, hierin werden die jeweligen Töne für die Farbbereiche
farbbereich = 0                                             #Welcher Farbton ist gerade oben gewählt (von 0 bis 7)
scrollLevel = 0                                             #Wie weit ist gerade im Lied gescrollt? von 0 bis ca. anzSpalten-1

#Zum Abspielen
playTon = 0         #Welcher Ton wird gerade gespielt?
tonLaenge = 500     #Wie lange ist der Ton (in Millisekunden)
playState = False   #Wird gerade gespielt oder nicht
taktEnde = 0        #Wann ist das nächste Taktende

#Zonen für den Zeiger
anzZonen = 1        #wie viele Bereiche gibt es?
akZone = -100       #in welcher Zone sind wir gerade (beginnend bei 0)      
zoning = False      #Ist der Servo gerade in Bewegung?
zoneTime = 350      #Wie lange hat der Servo Zeit sich anzupassen?
zoneEndTime = 0     #Was ist die aktuelle End-Servo-Zeit?

#Taktgeschichten
taktZahl = 4        #alle wie viele Takte schlägt der Taktservo aus?

# Fenster starten
window = pygame.display.set_mode((1800, 900))       #Die Fenstergröße ist vorgeschrieben und nicht änderbar. Das wäre ein Albtraum, das ganze auch noch skalierbar zu bauen, Web-Developer:innen können einem leid tun...
pygame.display.set_caption("Summchester")

#region Mal-Methoden
    #In diesen Methoden geht es darum, Inhalte auf den Bildschirm zu 'malen'
    #Um Performance zu erhöhen habe ich die enzelnde Bereiche unabhängig voneinander malenbar gemacht, dass nicht immer z.B. alle Töne gezeichnet werden müssen wenn ich nur die Geschwindigkeit erhöhen wollte
    #Einige Methoden haben deswegen den 'nur Elemente'-Parameter, wenn dieser auf True ist werden die Elemente nur 'vorbereitet' und dann von der allesMalen-Methode in einem gemalt, das müsste ein bisschen performanter sein. Man kann sie aber auch einzelnd malen, wenn 'nurElemente' auf False ist wrd auch direkt gemalt.

#Ich kommentiere einmal diese Methode ausführlich aus, diese Methoden sind im Kern eigentlich alle gleich. 
def kopfzeileMalen(nurElemente):
    #Zuerst wird der Bereich definiert, um den es geht. Diese Bereiche sind in konstanten.py zentral festgehalten, dass ich nicht so viele freilaufende zahlen im Code habe
    #In einem Moment spontaner Dummheit habe ich in konstanten.py zuerst die Dimesionen, dann die Koordianten der Fläche definiert. deswegen rufe ich da unten erste [x][1][x] und dann [x][0][x] auf, weil in pygame das immer anders herum ist. Naja, jetzt ist es so 'historisch gewachsen' und ich habe zu viel Angst es kaputt zu machen wenn ich jetzt etwas daran ändere.
    rectBereich = pygame.Rect(konstanten.bereiche[0][1][0],konstanten.bereiche[0][1][1],konstanten.bereiche[0][0][0],konstanten.bereiche[0][0][1])
    #Wenn die Methode nicht nur vorbereiten soll wird der definierte Bereich mit dem Hintergrundgrau (definiert in konstanten.py) gefüllt
    if(not nurElemente): pygame.draw.rect(window,konstanten.grauToene[0],rectBereich)

    #Der Stopp-Knopf wird zuerst an der definierten Position mit dem definierten Sprite belegt.
    window.blit(knop_kopf[0],konstanten.stButtons[0][0][0])

    #Der Start/Pause-Knopf wird ebenso belegt, abhängig davon in welchem playState wir gerade sind. Es wird immer das gegenteilige gezeigt (wenn das Lied gerade spielt wird ein Pauseknop angeboten)
    if(playState): knopp = 2
    else: knopp =1
    window.blit(knop_kopf[knopp],konstanten.stButtons[0][knopp][0])
    #wenn nicht nur vorbereitet werden soll wird alles gerade vorbereitete direkt auf das Display in der definierten Fläche gemalt. Der Bildschirminhalt ausserhalb wird nicht aktualisiert.
    if(not nurElemente): pygame.display.update(rectBereich)

#gleich wie kopfzeile, hier werden nur explizit Plus- und Minusknöpfe gesetzt weil ich keine Lust hatte, die als statische Knöpfe in den konstanten zu definieren
def kopfzeile2Malen(nurElemente):
    rectBereich = pygame.Rect(konstanten.bereiche[5][1][0],konstanten.bereiche[5][1][1],konstanten.bereiche[5][0][0],konstanten.bereiche[5][0][1])
    if(not nurElemente): pygame.draw.rect(window,konstanten.grauToene[0],rectBereich)

    #TonLaenge
    window.blit(sprite_Plus,(434,26))
    window.blit(sprite_Minus,(434,56))
    #Hier wird ausserdem ein Text mit [font].render geschrieben, der Text ist die aktuelle Tonlänge
    window.blit(font_big.render(str(tonLaenge),True,konstanten.grauToene[2]),(485,26))

    if(not nurElemente): pygame.display.update(rectBereich)

#nahezu indentisch zu kopfzeile2, nur dass es hier um die taktZahl geht
def kopfzeile3Malen(nurElemente):
    rectBereich = pygame.Rect(konstanten.bereiche[6][1][0],konstanten.bereiche[6][1][1],konstanten.bereiche[6][0][0],konstanten.bereiche[6][0][1])
    if(not nurElemente): pygame.draw.rect(window,konstanten.grauToene[0],rectBereich)

    #taktZahl
    window.blit(sprite_Plus,(854,26))
    window.blit(sprite_Minus,(854,56))
    window.blit(font_big.render(str(taktZahl),True,konstanten.grauToene[2]),(905,26))

    if(not nurElemente): pygame.display.update(rectBereich)

#Diese Methode hat keine 'nur Elemente'-Parameter, kann also nicht selbst malen sondern nur vornereiten, das liegt daran, dass zu Beginn des Programms sowieso immer allesMalen() aufgerufen wird und der Bereich kopfzeile4 nur statische Knöpfe hat, der Bereich muss also nie neu gezeichnet werden
def kopfzeile4Malen():
    for i,b in enumerate(konstanten.stButtons[2]):
        window.blit(knop_kopf4[i],b[0])

#Die komplexeste Mal-Methode, hier wird die Tabelle mit den Tönen gemalt
def hauptbereichMalen(nurElemente):
    global scrollLevel      #'global' heuißt immer, dass ich die variable des Skrips meine und keine eigene der Methode. So kann ich diese auch anpassen
    global anzSpalten
    global playTon

    #Bereich definieren und übermalen wenn gewünscht
    rectBereich = pygame.Rect(konstanten.bereiche[3][1][0],konstanten.bereiche[3][1][1],konstanten.bereiche[3][0][0],konstanten.bereiche[3][0][1])
    if(not nurElemente): pygame.draw.rect(window,konstanten.grauToene[0],rectBereich)
    
    #Der 'ScrollBonus' ist die relative Verschiebung in Pixeln, die durch das Scrollen mitberechnet werden muss, sobald 1 oder mehr gesrollt werden muss kommt die dunkelgraue Leiste, um den Scrollvorgang zu zeigen
    scrollBonus = 0
    if(scrollLevel>=1): 
        scrollBonus = 42
        #Markierungsspalte für den Scrollvorgang wird hier gemalt
        pygame.draw.rect(window,konstanten.grauToene[2],pygame.Rect(124,210,42,627))

    #hier werdden die leeren Spalten für die Töne gezeichnet, nach links auf das Scrollen begrenzt, nach recht theoretisch auch aus dem Bild heraus. Das schadet aber nicht mehrklich der Performance, deswegen habe ich es gelassen
    for x in range(anzSpalten):
        if(x>=scrollLevel):
            #Zur Erklärung: Die Tontabelle fängt bei x=124 an und ist 42 breit. 210 ist der y-Wert
            window.blit(sprite_Spalte,(scrollBonus+124+42*x-42*scrollLevel,210))

    #andere Noten einzeichnen
        #Jetzt werden alle Töne, Taktweise als grau eingezeichnet
    for i,e in enumerate(tonhalter):
        for j,t in enumerate(e):
            if(t != -1 and j>=scrollLevel):
                neuFeld = pygame.Rect(scrollBonus+anzZuBreite(j)-42*scrollLevel,tonZuHoehe(t),40,23)
                pygame.draw.rect(window,konstanten.grauToene[2],neuFeld)

    #Jetzt werden die Töne der aktuell selektierten Farbe in ihrer Farbe eingezeichnet
    #Die doppelte Schleife ärgert mich aber sonst ist nicht immer die Farbe oben
    for i,t in enumerate(tonhalter[farbbereich]):
        if(t != -1 and i>=scrollLevel):
            neuFeld = pygame.Rect(scrollBonus+anzZuBreite(i)-42*scrollLevel,tonZuHoehe(t),40,23)
            pygame.draw.rect(window,konstanten.farben[farbbereich],neuFeld)

    #Hier wird der Punkt, der den aktuellen takt symbolisiert, eingezeichnet
        #Aber nur, wenn er nicht im gerade weggescrollten Bereich liegt
    if(playTon>=scrollLevel):
        window.blit(sprite_Punkt,(scrollBonus+anzZuBreite(playTon)-42*scrollLevel+13,190))


    if(not nurElemente): pygame.display.update(rectBereich)

#aktualisiert nur den Punkt, der den gerade gespielten Takt anzeigt
def nurAkTonMalen():
    rectBereich = pygame.Rect(124,180,1676,29)
    pygame.draw.rect(window,konstanten.grauToene[0],rectBereich)

    scrollBonus = 0
    if(scrollLevel>=1): 
        scrollBonus = 42

    if(playTon>=scrollLevel):
        window.blit(sprite_Punkt,(scrollBonus+anzZuBreite(playTon)-42*scrollLevel+13,190))
    
    pygame.display.update(rectBereich)

#Hier wird der Bereich mit den Farbknöpfen und Plus- und Minusknöpfen für die Taktanzahl gezeichnet bzw. dafür vorbereitet
def farbwahlMalen(nurElemente):
    global farbbereich

    rectBereich = pygame.Rect(konstanten.bereiche[1][1][0],konstanten.bereiche[1][1][1],konstanten.bereiche[1][0][0],konstanten.bereiche[1][0][1])
    
    #Weil die Farbknöpfe nur aus Quadraten bestehen und ich keine Lust hatte, 8 Sprites zu malen werden die Knöpfe hier dynamisch generiert:

    for x in range(8):
        #je nachdem. ob die Farbe gerade ausgewählt ist kriegt der Rahmen eine andere Farbe/Dicke
        if(x==farbbereich):
            aussenfarbe = konstanten.grauToene[2]
            innenAbstand = 7
        else:
            aussenfarbe = konstanten.grauToene[1]
            innenAbstand = 4

        #Die Koordinaten des Rahmens, der Füllung und die Innendimensionen des Knopfes werden hier einmal mit Hilsvariablen berechnet, das hätte ich natürlich auch direkt in der Formel machen können aber das war nicht gesund für meinen Kopf
        aussenKoords = (22+66*x,115,50,50)
        innenDims = 50-2*innenAbstand
        innenKoords = (22+66*x+innenAbstand,115+innenAbstand,innenDims,innenDims)

        #Zuerst wird der Rahmen, dann die Füllung gemalt, beides als simple Rechtecke
        pygame.draw.rect(window,aussenfarbe,pygame.Rect(aussenKoords))
        pygame.draw.rect(window,konstanten.farben[x],pygame.Rect(innenKoords))
    
    #Ich bin mir nicht mehr ganz sicher, wieso hier die if-Abfrage ist aber es gab keine Probleme damit, deswegen lasse ich es jetzt so.
    if(nurElemente):
        window.blit(sprite_Plus,(594,115))
        window.blit(sprite_Minus,(594,145))  
    else: pygame.display.update(rectBereich)

#kein 'nurElemente' nötig, die Navleiste muss nur einmal gemalt werden und wird immer ber allesMalen() aufgerufen (so wie bei Kopfzeile4)
def navLeisteMalen():
    for i,b in enumerate(konstanten.stButtons[1]):
        window.blit(knop_nav[i],b[0])
    versionText = font_small.render("version "+version,True,konstanten.grauToene[1])
    window.blit(versionText,(1675,867))

#malt den gesamten Bildschirm. Hier ist zu beachten, dass alle unter-Mal-Methoden ihren 'nurElemte'-Parameter auf 'True' haben, selbst also nicht malen sondern nur vorbereiten
def allesMalen():

    #Das ganze Fenster wird übermalt
    window.fill((173,173,173))

    #Die Tabelle mit den Notennamen wird gemalt
    window.blit(sprite_Noten,(22,210))

    #Alle Mal-Untermethoden werden aufgerufen
    kopfzeileMalen(True)
    kopfzeile2Malen(True)
    kopfzeile3Malen(True)
    kopfzeile4Malen()
    hauptbereichMalen(True)
    farbwahlMalen(True)
    navLeisteMalen()

    #die Inhale werden alle auf dem Bildschirm angezeigt
    pygame.display.flip()

#Eine Malmethode, die den Hinweis, dass eine Karte an das Terminal gehalten werden soll, anzeigt.
    #Wird immer aufgerufen wenn der Kartenreader angesprochen wird und muss später mit der allesMalen()-Methode wieder übermalt werden.
def pauseMalen():
    window.blit(sprite_Pause,(22,14))
    pygame.display.flip()

#endregion Mal-Methoden

#region Zonen-Geschichten
    #Die Zonen sind eine Idee, um den Servo, der den Liedfortschritt anzeigt ein bisschen performanter zu machen. Dafür wird das gesamte Lied in maximal 9 Zonen einegteilt und der Servo bewegt sich nur wenn der aktuellle Takt in eine neue Zone übertritt
    #Ich hatte das zwischenzeitlich so, dass der Servo bei jedem Tatwechsel eine neue Position gekriegt hat, das lief aber einfach nicht gut, hat die ganze Zeit nur geruckelt und vom eigentlichen Lied abgelenkt.
    #Ich bin mit dieser Lösung jetzt halbwegs zufrieden, halte den Zonen-Servo aber für das schwächste Bauteil am ganzen Projekt.

#wird aufgerufen, wenn der Servo eine neue Zone anziegen soll. Der 'mehrZeit'-Parameter erlaubt mehr Zeit für den Übergang, wenn z.B. zum Liedanfang zurückgesprungen wird.
def neueZone(mehrZeit):
    global zoning
    global zoneEndTime

    #wenn es nur eine Zone gibt soll der Zeiger immer in der Mitte stehen. Außerdem kann es so nicht zu einer Nuldivison kommen
    if(anzZonen==1):zielProz = 0.5
    #hier ist zu bedenken, dass akZone bei 0 anfängt, anzZonen aber bei 1. Mit der Funktion kann so die Zone auf 0 bis 1 aufeschlüsselt werden
    else:zielProz = akZone/(anzZonen-1)

    servo.setProzent(zielProz)

    if(mehrZeit):zeitBonnus = 1200
    else: zeitBonnus = zoneTime

    #neuen Zeitpunkt setzen
    zoneEndTime = pygame.time.get_ticks()+zeitBonnus
    zoning = True

#Berechnet in welcher Zone der aktuelle playton ist und setzt akZone dementsprechend
def CalcAkZone():   
    global akZone
    #Formel um den playTon zu der aktuellen Zone zu matchen
    calZone = math.floor((playTon+1)/(anzSpalten/anzZonen))
    #Die aktuelle Zone darf natürlich nicht gleich die Anzahl der Zonen sein, weil das Erste bei 0 beginnt und das zweite bei 1
    if(calZone==anzZonen):calZone-=1
    
    #Hier wird geguckt ob sich die aktuelle Zone geändert hat
    #gleiche Zone
    if(calZone == akZone):
        pass    #nix passiert
    #wir sind in einer neuen Zone
    elif(abs(calZone-akZone)>1):    #sind wir von der ursprünglichen Zone weiter weg als 1? Wenn ja kriegt der Servo mehr Zeit seine Position zu ändern
        akZone = calZone
        neueZone(True)
    else:
        akZone = calZone
        neueZone(False)

#Berechnet wie viele Zonen es gibt
    #Es soll maximal 9 Zonen, kann aber auch weniger geben
def reCalcZones():
    global anzZonen
    if(anzSpalten<=8): anzZonen = anzSpalten
    else: anzZonen = 9
    CalcAkZone()

#endregion Zonen-Geschichten

#region Tonwiedergabe-Methoden
    #Alle Mehoden, die sich mit der tatsächlichen Wiedergabe des Liedes beschäftigen. Vom konkreten Spielen des Tons bis zum Koordinieren des Spielzustandes

#spielt für einen Takt alle Töne  
def taktSpielen(takt):
    for x in range(8):
        tonoutsource.starteTon(x,tonhalter[x][takt])

#Beendet die Tonwiedergabe
def taktBeenden():
    tonoutsource.stoppAlle()

#Schaltet die Tonwiedergabe auf den übergebenen Zustand
def togglePlay(soll):
    global playState
    global taktEnde

    playState = soll
    #print(playState)

    #Wenn der Zustand auf 'play' gesetzt werden soll
    if(playState):
        #neues taktende festlegen
        taktEnde = pygame.time.get_ticks()+tonLaenge
        #aktuellen Takt spielen
        taktSpielen(playTon)

    #Wenn der Zustand auf 'pause' gesetzt werden soll
    else:
        #Der takt-Servo wird gestoppt
        servo.stopTakt()
        #Die Wiedergabe wird beendet
        taktBeenden()
    
    #Die Kopfzeile wird aktualisiert, der Stopp-/Playknopf springt ja um
    kopfzeileMalen(False)

#Stoppt die komplette Wiedergabe und springt zurück
def StopPlay():
    global playTon
    global scrollLevel

    togglePlay(False)           #Wiedergabe auf 'stop'
    playTon = 0                 #Zum Anfang zurück
    scrollLevel =0              #Zum Anfang scrollen
    CalcAkZone()                #aktuelle Zone berechnen
    hauptbereichMalen(False)    #Hauptbereich neu malen (nicht Kopfzeile weil Stoppknopf sieht immer gleich aus)

#endregion Tonwiedergabe-Methoden

#region Hilfsrechen-Methoden
    #Hier werden ein paar Hilfsmethoden ausgelagtert, die häufig genutzte Berechnungen abbilden

#nimmt als input eine Hähe in pixel auf dem Bildschirm und gibt den dazu gehörenden Ton als Zahl von 0 bis ca. 24 zurück
def hoeheZuTon(hoehe):
    #wenn die übergebene Höhe über/unter den Tonhöhen ist wird -1 zurückgegeben
    if(hoehe<211 or hoehe>835):
        return -1
    
    #Um die Berechnung einfacher zu machen wird die reative Höhe gebilet, dass der Zahlenbereich von 0 bis ca. 624 geht
    relHoehe = hoehe -211
    if(relHoehe == 0): return 24
    else:
        #Die oberen Töne sind höher, die Liste ist aber tief -> hoch sortiert, das Ergebnis muss also umgedreht werden. Ein Ton ist 24 pixel hoch
        return 24-(int)(relHoehe/25)

#nimmt als input eine Brete in pixel auf dem Bilrschirm und gibt den dazughörigen Takt aus.
def breiteZuAnz(breite):
    global scrollLevel              #Das könnte eigentlich weg

    if(scrollLevel<0): pass         #Das könnte eigentlich auch weg
    if(breite<124): return -1       #Wenn die x-Koordinate links von der Tontabelle liegt wird -1 zurückgegeben
    else:
        #läuft eigentlich gleich ab wie hoeheZuTon(), mit der relativen Position, muss aber nicht umgedreht werden
        relBreite = breite-124      
        if(relBreite==0): return 0
        else:
            return (int)(relBreite/42)

#Gibt für eine Breite zurück, welcher Farbknopf gedrückt wurde
def breiteZuFarbknopf(breite):
    relPos = breite -22             #Wieder mit der relativen Breite, dass die Zahl bei 0 anfängt
    sektor = (int)(relPos/66)       #In welchem groben Knopfbereich(='sektor') liegt die Breite?
    if(sektor>7): return -1         #kann ka maximal 7 sein, beginnt bei 0 und gibt 8 Knöpfe

    #ist in dem berechneten Sektor die Breite auch wirklich auf dem knopf? Da sind ja Lücken dazwischen...
    if(relPos%66<=50):return sektor
    else: return -1


#gibt zu einem Ton (0-24) die entprechende Pixelhöhe zurück
def tonZuHoehe(ton):
    if(ton<0 or ton>24): return -1      #liegt die Eingabe im erlaubten Bereich?
    else: return 812-ton*25             #Umrechnung und Rückgabe


#gibt zu einem Takt die entsprechende Pixelbreite zurück
def anzZuBreite(anz):
    if(anz<0): return -1
    else: return 125+anz*42             #Umrechnung und Rückgabe

#endregion Hilfsrechen-Methoden

#region Scroll-Methoden
    #Das Scrollen erlaubt die Verschiebung der Takte um das ganze Lied darstellen zu können

#Schiebt das Lied je nach Parameter nach links oder rechts 
def Scrollen(richtung):
    global scrollLevel

    #richung = 1 -> Lied verschiebt sich nach links
    if(richtung == 1 and scrollLevel < anzSpalten-1):
        scrollLevel += 1
    #richtung = -1 -> Lied verschiebt sich nach rechts
    elif(richtung == -1 and scrollLevel > 0):
        scrollLevel -= 1
    #print("neues Scrolllevel: ",scrollLevel)
    #Hauptbereich muss natürlich neu gemalt werden
    hauptbereichMalen(False)

#schiebt das Lied ganz nach Rechts, gamz links ist also der Anfang des Liedes
def ScrollBeginn():
    global scrollLevel

    scrollLevel = 0
    hauptbereichMalen(False)

#Hier hatte ich es ursprünglich so, dass das Lied ganz nach links geschoben wurde. Das mach aber wenig Sinn, ich habe es jetzt so umgebaut, dass es so verschoben wird, dass der rechte Liedrand gerade noch auf den Bildschirm passt
def ScrollEnde():
    global scrollLevel

    #Hintergrund: ca. 39 Takte passen auf den Bildschirm, wenn es so viele oder weniger Takte gibt kann das Lied also nach ganz rechts geschoben werden
    if(anzSpalten<=39):level = 0
    #Ansonsten so, dass der rechte Rand gerade noch so drauf ist
    else:level = level = anzSpalten -38
    scrollLevel = level
    hauptbereichMalen(False)

#endregion Scroll-Methoden

#region Globale Variablen ändern
    #Manche Methoden ändern globale Variablen. Das hat manchmal größere Auswirkungen als nur die Änderung selbst, dafür gibt es diese Methoden.

#Ändert die gerade gewählte Farbe (bereich=[0-7])
def TonbereichWechsel(bereich):
    global farbbereich 

    farbbereich = bereich       #Variabel ändern
    farbwahlMalen(False)        #Knöpfe neu malen
    hauptbereichMalen(False)    #Takte neu malen, jetzt gibt es ja eine andere Farbe

#Ändert die Anzahl der Spalten (Anzahl der Takte). Setzt nicht explizit den neuen Wert sondern erhöht/senkt um 1, je nach Parameterwert
def SpatenAendern(wat):     #Der Rechtschreibfehler ist mir zu spät aufgefallen, das heißt jetzt so
    global anzSpalten
    global scrollLevel
    global playTon

    #wat = -1 -> Eine Spalte weg
    if(wat ==-1 and anzSpalten>1):
        anzSpalten -= 1
        for bereich in tonhalter:
            #jedem Farbbereich wird der Ton am Ende weggenommen
            bereich.pop()
    #wat = 1 -> Eine Spalte dazu
    elif(wat == 1):
        anzSpalten += 1
        for bereich in tonhalter:   
            #jedem Farbbereich wird ein Ton (vorbelegt = -1 -> kein Ton) hinzugefügt
            bereich.append(-1)
    
    #Wenn es gerade ganz nach links gescrollt war muss das Lied um eins nach rechts verschoben werden
    if(scrollLevel>=anzSpalten):
        scrollLevel = anzSpalten -1

    #wenn der aktuelle Ton gerade ganz rechts war muss er auch um eins nach links verschoben werden
    if(playTon >=anzSpalten):
        playTon -= 1

    reCalcZones()               #Die Zonen müssen neu berechnet werden
    hauptbereichMalen(False)    #Der Hauptbereich wird neu gemalt

#Ändert die Tonlänge, wieder nicht explizit sondern +/- 10
def tonLaengeAendern(wat):
    global tonLaenge

    if(wat==1): tonLaenge+=10
    elif(wat==-1 and tonLaenge > 70): tonLaenge-=10
    print("neue Tonlänge: ",tonLaenge)
    #in Kpfzeile2 steht die Tonlänge
    kopfzeile2Malen(False)      

#Fast identisch zu tonLaengeAendern(), nur mit taktZahl
def taktZahlAendern(wat):
    global taktZahl

    if(wat==1): taktZahl+=1
    elif(wat==-1 and taktZahl > 1): taktZahl-=1
    kopfzeile3Malen(False)

#endregion Globale Variablen ändern

#region Speichern/Laden
    #Die Lieder können über NFC-Karten gespeichert und geladen werden. Tatsächich werden die Lieder lokal auf dem Gerät unter Lieder/[name].irk gespeichert, die Karte ist der Schlüssel, der den Namen trägt

#Methode um ein Lied zu speichern
def LiedSpeichern():
    togglePlay(False)                                           #Wiedergabe pausieren
    pygame.display.set_caption("Summchester - Lied speichern")  #Titel ändern
    pauseMalen()                                                #Hinweis auf Bildschirm malen

    #Das Kartenlesegerät muss rauskriegen wie der text lautet
    text = kartenGeschichten.KarteLesen()

    #Wenn das Gerät etwas gefunen hat
    if(text is not None):
        saveHandler.saveAs(text,tonhalter,tonLaenge,taktZahl)   #Das Lied wird gespeichert
        pygame.display.set_caption("Summchester - "+str(text))  #Der Programmtitel wird angepasst um die Anwender:in auf das erfolgreiche Speichern hinzuweisen
    else: pygame.display.set_caption("Summchester")             #Wenn es nicht geklappt hat steht oben nur "Summchester"
    allesMalen()                                                #Der Hinweis muss übermalt werden

#Methode um ein gespeichertes Lied zu laden
def LiedLaden():
    global tonLaenge, tonhalter,taktZahl, anzSpalten, playTon, scrollLevel, playState

    togglePlay(False)                                           #Wiedergabe pausieren
    pygame.display.set_caption("Summchester - Lied laden")      #Titel ändern
    pauseMalen()                                                #Hinweis auf den Bildschirm malen

    #Das Kaertenlesegerät muss rauskriegen wie der Text lautet
    text = kartenGeschichten.KarteLesen()

    #Wenn das Gerät etwas gefunden hat
    if(text is not None):
        erg1, erg2, erg3 = saveHandler.openFrom(text)           #hilsvariablen mit dem Inhalt aus der Datei mit name=[text].irk belegen
        if(erg1 is not None and erg2 is not None):              #wenn die Belegung funktioniert hat geht es weiter:
            pygame.display.set_caption("Summchester - "+text)       #Der Programmtitel wird angepasst um die Anwender:in auf das erfolgreiche Laden hinzuweisen
            tonLaenge = erg1                                        #Tonlänge belegen
            tonhalter = erg2                                        #Die eigentlichen Töne belegen
            taktZahl = erg3                                         #Taktzahl belegen
            anzSpalten = len(tonhalter[0])                          #Spaltenanzahl belegen
            playTon = 0                                             #An den Anfang des Liedes springen
            scrollLevel = 0                                         #An den Anfang des Liedes scrollen
            playState = False                                       #Wiedergabe auf 'pause' setzen
            reCalcZones()                                           #Zonen neu berechnen
        else: pygame.display.set_caption("Summchester")         #Wenn es nicht geklappt hat steht oben nur "Summchester"
    
    allesMalen()                                                #Der Hinweis muss übermalt werden

#endregion Speichern/Laden

#region click-Methoden
    #Methoden, die etwas mit dem Klicken auf Elemente zu tun haben

#Das war ursprünglich die ganze Kopfzeile, jetzt ist es nur noch der Bereich mit dem Stop- und den Play-/Pauseknöpfen
def clickOnKopfzeile(pos):

    #Welche der Knöpfe wurden gedrückt?
    if(pos[1]>=konstanten.stButtons[0][0][0][1] and pos[1]<konstanten.stButtons[0][0][0][1]+75):
        #Stoppknopf:
        if(pos[0]>=konstanten.stButtons[0][0][0][0] and pos[0]<konstanten.stButtons[0][0][0][0]+75):
            StopPlay()
        #Play-/Pausenopf
        elif(pos[0]>=konstanten.stButtons[0][1][0][0] and pos[0]<konstanten.stButtons[0][1][0][0]+75):
            togglePlay(not playState)

#In dem Bereich kann die Tonlänge geändert werden. Es wird geschaut ob auf die kleinen Plus-/Minusknöpfe gedrückt wurde
def clickOnKopfzeile2(pos):

    if(pos[0]>=434 and pos[0]<454):
        if(pos[1]>=26 and pos[1]<46):
            tonLaengeAendern(1)
        elif(pos[1]>=56 and pos[1]<76):
            tonLaengeAendern(-1)

#In dem Bereich kann die Taktzahl geändert werden. Es wird geschaut ob auf die kleinen Plus-/Minusknöpfe gedrückt wurde
def clickOnKopfzeile3(pos):

    if(pos[0]>=854 and pos[0]<874):
        if(pos[1]>=26 and pos[1]<46):
            taktZahlAendern(1)
        elif(pos[1]>=56 and pos[1]<76):
            taktZahlAendern(-1)

#In diesem Bereich steht der Import- und Exportknopf
def clickOnKopfzeile4(pos):
    if(pos[1]>=konstanten.stButtons[2][0][0][1] and pos[1]<konstanten.stButtons[2][0][0][1]+75):
        knoppNr = -1
        for i in range(len(konstanten.stButtons[2])):
            if(pos[0]>=konstanten.stButtons[2][i][0][0] and pos[0]<konstanten.stButtons[2][i][0][0]+150):
                knoppNr = i
                break
        
        if(knoppNr == 0):LiedSpeichern()
        elif(knoppNr == 1):LiedLaden()

#In diesem Bereich stehen die Farbknöpfe und die Knöpfe um die Taktzahl zu ändern
def clickOnFarbwahl(pos):
    if(pos[1]>=115 and pos[1]<165 and pos[0]<574):
        KnoppNummer = breiteZuFarbknopf(pos[0])
        if(KnoppNummer != -1): TonbereichWechsel(KnoppNummer)

    if(pos[0]>=594 and pos[0]<614 and pos[1]>=115 and pos[1]<135): SpatenAendern(1)
    elif(pos[0]>=594 and pos[0]<614 and pos[1]>=145 and pos[1]<165): SpatenAendern(-1)


#Das ist der eigentliche Hauptbereich mit den Tönen
def clickOnHaupt(pos):
    global scrollLevel
    global playTon

    #Zuerst wird ausgerechnet welcher um welchen Ton und welchen Takt es sich handelt
    gewTon = hoeheZuTon(pos[1])
    gewAnz = breiteZuAnz(pos[0])

    #der takt wir über abolute Positionen berechnet und wird hier an das Scrollevel angepasst
    if(scrollLevel>=2): gewAnz += scrollLevel -1

    #Wenn der Takt gerade im 'weggescrollten' Bereich liegt wird der Ton auf ungültig gesetzt
    if(scrollLevel>=1 and gewAnz<scrollLevel): gewTon = -1

    #wenn der Klick über der eigentlichen Tabelle liegt wird der gewählt Takt genutzt um den playTon-Indikator zu setzen
    if(pos[1]>=190 and pos[1]<210 and gewAnz<anzSpalten and gewAnz>=scrollLevel):
        playTon = gewAnz
        togglePlay(playState)
        CalcAkZone()
        hauptbereichMalen(False)
        return None

    #print("Ton ",gewTon," an Position ",gewAnz)

    #Der Ton muss einen Wert haben und im erlaubten Bereich sein
    if(gewTon!=-1 and gewAnz<anzSpalten):
        #akTon wrd mit dem aktuellen Ton belegt
        akTon = tonhalter[farbbereich][gewAnz]
        #Wenn auf einen Ton geklickt wurde, der da schon ist, wird er entfernt.
        if(akTon!=-1 and akTon==gewTon):tonhalter[farbbereich][gewAnz] = -1
        #Ansonsten kommt da der neue Ton hin
        else: tonhalter[farbbereich][gewAnz] = gewTon
        hauptbereichMalen(False)

#In diesem Bereich steht die Navigationszeile zum Scrollen
def clicOnFuss(pos):
    #Abfrage auf y-Koordinatenbereich
    if(pos[1]>=konstanten.stButtons[1][0][0][1] and pos[1]<konstanten.stButtons[1][0][0][1]+40):
        knoppNr = -1
        #Abfrage auf x-Koordinatenbereich über die stButtons in den konstanten
        for i in range(len(konstanten.stButtons[1])):
            if(pos[0]>=konstanten.stButtons[1][i][0][0] and pos[0]<konstanten.stButtons[1][i][0][0]+40):
                knoppNr = i
                break
        
        #Zuweisung des gwählten Knopfes zur Methode
        if(knoppNr == 0):ScrollBeginn()
        elif(knoppNr == 1):Scrollen(-1)
        elif(knoppNr == 2):Scrollen(1)
        elif(knoppNr == 3):ScrollEnde()

#Die erste Methode, die aufgerufen wird, wenn auf den Bildschirm geklickt wird. Darin wird entschieden, um welchen Bereich es geht und die entsprechende Unterklickmethode aufgerufen
#Ich versuch damit so ein bisschen ein 'Teile-und-Herrsche'-Prinzip anzuwenden, es ist perfomanter bereichsspezifisch vorzugehen als in jedem Frame jeden Knopf fragen zu lassen 'wurde ich gerade geklickt?'
def clickhandler(pos):
    #print("click on ",pos[0],",",pos[1])
    #Die in konstanten efinierten Bereich werden durchgegangen und die Dimensionen gegen die Mausposition abgeglichen
    for i,e in enumerate(konstanten.bereiche):
        if(pos[0]>=e[1][0] and pos[0]<=e[1][0]+e[0][0] and pos[1]>=e[1][1] and pos[1]<=e[1][1]+e[0][1]):
            print(e[2]," bzw. Position ",i)
            if(i==0): clickOnKopfzeile(pos)
            elif(i==1): clickOnFarbwahl(pos)
            elif(i==2): 
                #print(hoeheZuTon(pos[1]))
                #Hier habe ich gar keine eigee Methode geschrieben, wenn man auf eine Tonbescheibung klickt wird der Ton kurz gespielt
                tonoutsource.zeigTon(farbbereich,hoeheZuTon(pos[1]))
            elif(i==3): clickOnHaupt(pos)
            elif(i==4): clicOnFuss(pos)
            elif(i==5): clickOnKopfzeile2(pos)
            elif(i==6): clickOnKopfzeile3(pos)
            elif(i==7): clickOnKopfzeile4(pos)
            break

#endregion click-Methoden

#Diese Methoden werden beim Programmstart aufgerufen
allesMalen()
reCalcZones()

# region Game-loop
    #Der sogenannte Game-loop ist eine endlosschleife, die während das Programm offen ist, ständig durchlaufen wird. Hier werden Nutzereingaben registriert und Ausgaben können gesteuert werden
running = True  #Die Variable, die steuert, ob die Schleife läuft.
while running:
    #ein event in pygame kann in diesem Fall ein Klick ins Fenster, ein Tastendruck oder der Klick auf den 'Fenster-schließen'-Knopf sein
    for event in pygame.event.get():
        #Wenn ich auf 'Fenster-schließen' drücke geht das Programm zu
        if event.type == pygame.QUIT:
            running = False
        #Hier habe ich ein paar Tastenkürzel eingebaut. Die sind aber optional, das Programm kann komplett über die Maus genutzt werden
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS: SpatenAendern(1)
            elif event.key == pygame.K_PERIOD : SpatenAendern(-1)
            elif event.key == pygame.K_SPACE: togglePlay(not playState)
            elif event.key == pygame.K_UP: Scrollen(1)
            elif event.key == pygame.K_DOWN: Scrollen(-1)
            elif event.key == pygame.K_LEFT: ScrollBeginn()
            elif event.key == pygame.K_RIGHT: ScrollEnde()
            elif event.key == pygame.K_o: tonLaengeAendern(-1)
            elif event.key == pygame.K_p: tonLaengeAendern(1)
            elif event.key == pygame.K_1: TonbereichWechsel(0)
            elif event.key == pygame.K_2: TonbereichWechsel(1)
            elif event.key == pygame.K_3: TonbereichWechsel(2)
            elif event.key == pygame.K_4: TonbereichWechsel(3)
            elif event.key == pygame.K_5: TonbereichWechsel(4)
            elif event.key == pygame.K_6: TonbereichWechsel(5)
            elif event.key == pygame.K_7: TonbereichWechsel(6)
            elif event.key == pygame.K_8: TonbereichWechsel(7)
            elif event.key == pygame.K_ESCAPE: StopPlay()
            
            #Hier wird ein Linksklick auf den Bildschirm abgefragt 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clickhandler(event.pos)
    
    #Für den späteren Bereich brauchen wir einen aktuellen Zeitpunkt, hier wird akZeit mit den bereits gelaufenden Ticks belegt
    akZeit = pygame.time.get_ticks()

    #wenn der ZonenWechsel abgeschlossen ist
    if(zoning and akZeit>=zoneEndTime):
        servo.stopProzent()
        zoning = False

    #wenn gerade der Status auf "play" ist
    if(playState):
        #Ende des taktes ist erreicht
        if(akZeit>=taktEnde):

            #wenn rechts noch Platz ist
            if(playTon<anzSpalten-1):
                #es geht rechts weiter
                playTon += 1
                

            #wir sind im letzen Takt des Liedes
            else:
                #es geht zurück an den Anfang
                playTon = 0

            #Neues Taktende festlegen
            taktEnde = akZeit+tonLaenge
            taktBeenden()
            taktSpielen(playTon)

            #Hier wird der Taktservo getriggert wenn es wieder so weit sein sollte
            if(playTon%taktZahl==0):servo.toggleTakt()

            #Aktuelle Zone neu berechnen
            CalcAkZone()

            nurAkTonMalen()

# endregion Game-loop

#Dieser Bereich kommt wenn das Programm beendet wird.

#stoppt alle Töne und mach ein gpio.cleanup
tonoutsource.reicht()

#beendet Pygame
pygame.quit()