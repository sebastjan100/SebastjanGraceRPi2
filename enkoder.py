#uvozimo knjižnico za delo z GPIO pini
from RPi import GPIO

step = 5 #shranimo korak, ki ga prištejemo ali odštejemo, ko se zavrti enkoder
counter = 0 #števec, začnemo šteti z 0
paused = False #spremljamo stanje, kdaj se ustavimo

def initialize(clk, dt, sw):
    #Nastavimo vhodne in izhodne enote
    #GPIO.setup(pin, vhod/izhod, način)
    GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    #Prevri in nastavimo prvotno stanje
    
    #clkLastState = GPIO.input(clk) #preberamo stanej na pinu 17 - S2
    #dtLastState = GPIO.input(dt) #preberamo stanej na pinu 18 - S1
    #swLastState = GPIO.input(sw) #preberamo stanej na pinu 27 - KEY

    #na začtku sprintano začetna stanja                
    #print ("Initial clk:", clkLastState)
    #print ("Initial dt:", dtLastState)
    #print ("Initial sw:", swLastState)
    #print ("=========================================")

#define functions which will be triggered on pin state changes
    
def clkKlik(clk, dt):
    def clkClicked(channel):
        global counter #uporabimo globalno spremenljivko counter
        global step    #uporabimo globalno spremenljivko step

        clkState = GPIO.input(clk) #preberamo stanej na pinu 17 - S2
        dtState = GPIO.input(dt) #preberamo stanej na pinu 18 - S1

        #Premikamo se v smeri urinega kazalce, če je pin 17 == 0 in pin 18 == 1
        if clkState == 0 and dtState == 1:
            #prištejemo korak - vrtimo se v smeri urinega kazalca
            counter = counter + step
            print ("Counter ", counter)
    return clkClicked

def dtKlik(clk, dt):
    def dtClicked(channel):
        global counter #uporabimo globalno spremenljivko counter
        global step    #uporabimo globalno spremenljivko step

        clkState = GPIO.input(clk) #preberamo stanej na pinu 17 - S2
        dtState = GPIO.input(dt)   #preberamo stanej na pinu 18 - S1
        
        #Premikamo se v obratni smeri urinega kazalce, če je pin 17 == 1 in pin 18 == 0
        if clkState == 1 and dtState == 0:
            #odštejemo korak - vrtimo se v obratni smeri urinega kazalca
            counter = counter - step
            print ("Counter ", counter)
    return dtClicked


def swClicked(channel):
    global paused #povemo da bomo uporabili globano spremenljivko
    paused = not paused #obrnemo vrednost spremenjivke paused
    print ("Paused ", paused)             

def getCounter():
    global counter
    return counter

def getClick():
    global paused
    return paused

#clk in dt sta spremeljivki, ki povesta kam smo povezali pina enkoderja (S1, S2)
#sw je spremenljivka, ki pove kam je povezana tipka (Key)


if __name__ == "__main__":
    #Natsavimo prekintve
    #GPIO.add_event_detect(pin, kdaj preberemo FALLING/RISING/ONCHANGE, kaero funkijo naj izvede prekinitev, nastaviko koliko časa naj prekinitev počaka prad ponovno izvedbo )
    clk = 17
    dt = 5
    sw = 27



    initialize(clk, dt, sw)
    GPIO.add_event_detect(clk, GPIO.FALLING, callback=clkKlik(clk, dt), bouncetime=100)
    GPIO.add_event_detect(dt, GPIO.FALLING, callback=dtKlik(clk, dt), bouncetime=100)
    GPIO.add_event_detect(sw, GPIO.FALLING, callback=swClicked, bouncetime=300)

    input("Start monitoring input")

    #Počistimo nastavitve vseh pinov
    #GPIO.cleanup()
