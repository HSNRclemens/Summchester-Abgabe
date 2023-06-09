import RPi.GPIO as gpio
import time
import math

import konstanten

#Der Taktsevo sprint immer zwischen 5 und 9 hin und her. Es beginnt bei (willkürlich gewählt) 5
takt = 5

gpio.setmode(gpio.BOARD)

#Der Prozentservo
    #Zeigt den Liedfortschritt. Ist der sichtbare Output aller 'Zonen'-Operationen
gpio.setup(konstanten.servos[0],gpio.OUT)
p = gpio.PWM(konstanten.servos[0],50)

#Der Taktservo
    #Sprint im gewählten Taktmuster hin und her
gpio.setup(konstanten.servos[1],gpio.OUT)
t = gpio.PWM(konstanten.servos[1],50)

#nimmt eine Prozentzahl (0.00 bis 1.00) an und stellt den Prozentservo auf die Zahl ein
def setProzent(prozent):
    if(prozent<0 or prozent>1): return None
    else:
        #2 = 100%, 12 = 0%, das sah so in der Anzeige schlüssiger aus
        p.start(12-10*prozent)

#hält den Zeiger an der aktuellen Position fest. Verhindert das Zittern, in das er sonst leider verfällt.
def stopProzent():
    p.ChangeDutyCycle(0)

#wechselt die takt-variable
def toggleTakt():
    global takt

    #5 -> 9 und 9 -> 5 
    takt += math.copysign(4,8-takt)
    t.start(takt)

#hält den Taktservo an
def stopTakt():
    t.ChangeDutyCycle(0)