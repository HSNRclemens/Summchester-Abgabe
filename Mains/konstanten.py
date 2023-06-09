#Diese Datei ist die Auslagerung aller konstanten Werte, die gebraucht werden.
    #Ich hätte das auch gleich in meinem Hauptskript schreiben können aber spätestens wenn andere Nebenskripte auch auf Werte zugeifen macht es für mich so mehr Sinn

#Die Bereiche mit (Größe,Koordinatem,Name). Das war so in der Reihenfolge sehr unklug, überall sonst ist zuerst die Position, dann die Größe aber als mir das auffiel war es schon in Methoden vercodet und ich wollte nicht riskieren etwas kaputt zu machen
bereiche = (((420,100),(0,0),"Kopfzeile1"),
            ((1800,80),(0,100),"Farbbereiche"),
            ((124,670),(0,180),"Tonwahl"),
            ((1676,670),(124,180),"Hauptbereich"),
            ((1800,50),(0,850),"Fußzeile"),
            ((420,100),(420,0),"Kopfzeile2"),
            ((420,100),(840,0),"Kopfzeile3"),
            ((540,100),(1260,0),"Kopfzeile4"))

#Die Frequenzen, die die Piezo-Summer über PWM eingespielt kriegen müssen um den richtigen Ton zu spielen.
toene = (131,141,149,163,169,181,191,203,216,228,243,256,272,290,308,325,346,368,390,415,442,466,500,528,560)

#Die 8 auswählbaren Farben
farben = ((87,120,93),
          (49,69,130),
          (205,83,90),
          (215,187,104),
          (178,98,218),
          (101,190,212),
          (154,35,98),
          (197,114,40),
          (65,65,65))

#Die 3 häufig genutzen Grautöne von der Hintergrundfarbe bis zur starken Akzentfarbe
grauToene = ((173,173,173),(144,144,144),(84,84,84))

#Die 8 Pins auf denen die Piezo-Summer sitzen
pins = (29,31,33,35,37,36,38,40)

#Die 2 Pins, auf der die Servos sitzen
servos = (8,10)

#Auflistung der statischen Knöpfe für besseres Zeichnen und Klickerkennung via Code
stButtons =((((22,14),"StoppKnopp.png"),
            ((130,14),"PlayKnopp.png"),
            ((130,14),"PauseKnopp.png")),

            (((22,854),"navBackEnd.png"),
            ((72,854),"navBack.png"),
            ((152,854),"navWeiter.png"),
            ((202,854),"navWeiterEnd.png")),

            (((1274,14),"KarteExport.png"),
            ((1470,14),"KarteImport.png")))