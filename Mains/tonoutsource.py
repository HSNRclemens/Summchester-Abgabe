import RPi.GPIO as gpio
#import PC_Version as gpio      #
import time
import konstanten

gpio.setmode(gpio.BOARD)

#Weil 8 davon gebraucht werden schreine ich sie in eine Liste um Platz zu sparen
pwms = []

#Die Piezo-pins durchgehen und für jeden eine pwm-instanz anlegen
for p in konstanten.pins:
    gpio.setup(p, gpio.OUT)
    pwm = gpio.PWM(p, 1)
    pwms.append(pwm)

#Startet den Ton für einen bestimmten Summer
def starteTon(wer,ton):
    if(ton is not -1):
        pwms[wer].ChangeFrequency(konstanten.toene[ton])
        pwms[wer].start(0.3)

#Stoppt einen bestimmten Summer
def stoppeTon(wer):
    pwms[wer].stop()

#Spielt kurz den Ton
def zeigTon(wer,ton):
    starteTon(wer,ton)
    time.sleep(0.3)
    stoppeTon(wer)

#Macht alle Summer aus
def stoppAlle():
    for x in range(8):
        stoppeTon(x)

#Beendet alle Wiedergaben
def reicht():
    stoppAlle()
    gpio.cleanup()