import RPi.GPIO as GPIO
import time
import random
import pygame
import music
import uz as UZ #ultasonic senzor knjiznica
import dht as DHT #DHT sen knjiznica
import Adafruit_SSD1306 #display knjiznica
from PIL import Image, ImageDraw, ImageFont     #objekti za izrisovanje na display
#import subprocess #knjižnica za dostop do kernal procesov
import enkoder
import send
import pir
import board
import neopixel
from settings import *

# Inicializacija LED stripa
strip_len= 5
if DEBUG:
    print("initialize LED strip")
pixels = neopixel.NeoPixel(board.D21, strip_len)

GPIO.setmode(GPIO.BCM)

##### VNESI SVOJE PODATKE #####
url = "https://gracewebapp-sebastjantekavc.online404.repl.co"
apikey = "sebastjan"
###############################

# Display inicializacija:
RST = None     # on the PiOLED this pin isnt used
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST) # 128x32 display with hardware I2C:
disp.begin() # Initialize library.
disp.clear() # Clear display.
disp.display() # Clear display.

#Priprava OLED ekrana
# Create blank image for drawing.
if DEBUG:
    print("initialize OLED display")
width = disp.width
height = disp.height
image = Image.new('1', (width, height)) # Make sure to create image with mode '1' for 1-bit color.
draw = ImageDraw.Draw(image) # Get drawing object to draw on image.
draw.rectangle((0,0,width,height), outline=0, fill=0)# Draw a black filled box to clear the image.
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
x = 0 # Move left to right keeping track of the current x position for drawing shapes.
font = ImageFont.load_default() # Load default font.

#Inicializacija UZ senzorja
trig = 26
echo = 19
if DEBUG:
    print("initialize UZ")
UZ.initialize(trig, echo) 

#Inicializacija DHT senzorja
dht_pin = 4
if DEBUG:
    print("initialize DHT")
DHT.setDHT_pin(dht_pin)


#Nastavimo spremenljivke za pine enkoderja
clk = 5
dt = 17
sw = 27

#Nastavimo spremenljivko PIR senzorja
pir_pin = 13

############################################# RGB def
num_pixels = 5
ORDER = neopixel.GRB

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)



#lokalne vrednosti za musko
currentLink = ""
playing = False


try: 
    #Inicializiramo enkoder
    if DEBUG:
        print("initialize Encoder")
    enkoder.initialize(clk, dt, sw)

    #Nastavimo "interupt" funkcije za enkoder
    GPIO.add_event_detect(clk, GPIO.FALLING, callback=enkoder.clkKlik(clk, dt), bouncetime=100)
    GPIO.add_event_detect(dt, GPIO.FALLING, callback=enkoder.dtKlik(clk, dt), bouncetime=100)
    GPIO.add_event_detect(sw, GPIO.FALLING, callback=enkoder.swClicked, bouncetime=300)

    #Inicializiramo PIR senzor
    if DEBUG:
        print("initialize PIR")

    #Nastavimo "interupt" funkcijo za PIR senzor
    pir.initialize(pir_pin)
    GPIO.add_event_detect(pir_pin, GPIO.FALLING, callback=pir.pirMove(pir_pin), bouncetime=100)

    #LED strip obarvamo belo
    if DEBUG:
        print("Set led strip to some color")
    for i in range(strip_len):
        pixels[i] = (120,0,120)

    #pygame init
    pygame.mixer.init()
    
    while True:
        #Napišemo prazno povešino za izpis na ekran
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        #Pridobitev IP naslova
        #cmd = "hostname -I | cut -d\' \' -f1"
        #IP = subprocess.check_output(cmd, shell = True )
        #draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)

        #Pridobivanje podatkov iz PIR sezorja
        time_of_last_move = pir.getLastMove()
        #Izpis stanja PIR senzorja
        if time_of_last_move == None: #Ni premika
                draw.text((x, top),  "No movement!" ,  font=font, fill=255)
                if enkoder.paused == False:
                    barva = send.TRAK(url, "/api/ledtrak/barva/", apikey)
                    r1 = int(barva[1:3], 16)
                    g1 = int(barva[3:5], 16)
                    b1 = int(barva[5:7], 16)
                    print(r1,g1,b1)
                    for i in range(strip_len):
                        pixels[i] = (r1,g1,b1)
                elif enkoder.paused == True:
                    rainbow_cycle(0.001)

        elif time.time() - time_of_last_move < 10: #Je zaznan premik v zadnjih 10 sekundah
            #LED strip obarvamo rdeče
            if DEBUG:
                print("set LED strip to RED")
            for i in range(strip_len):
                    pixels[i] = (255, 0, 0)
            cas = time.localtime( time_of_last_move )
            #Izpišemo čas zadnjega premika
            draw.text((x, top),  "Last move: " + str(cas[3])+":"+str(cas[4])+":"+str(cas[5]) ,  font=font, fill=255)
                
        else:
            #ledtrak
            
            #Več kot 10s ni bilo premika
            if DEBUG:
                print("set LED strip to color that was before")
            if enkoder.paused == False:
                barva = send.TRAK(url, "/api/ledtrak/barva/", apikey)
                r1 = int(barva[1:3], 16)
                g1 = int(barva[3:5], 16)
                b1 = int(barva[5:7], 16)
                print(r1,g1,b1)
                for i in range(strip_len):
                    pixels[i] = (r1,g1,b1)
            elif enkoder.paused == True:
                rainbow_cycle(0.001)
            #Izpišemo čas zadnjega premika
            cas = time.localtime( time_of_last_move )
            draw.text((x, top),  "Last move: " + str(cas[3])+":"+str(cas[4])+":"+str(cas[5]) ,  font=font, fill=255)
        #Pridobimo in izpišemo podatke UZ senzorja
        if DEBUG:
            print("read UZ")
        razd = UZ.distance(trig, echo)
        if DEBUG:
            print("Izmerjena razdalja je", razd, "cm.")
        draw.text((x, top+8),  "Razdalja:" + str(round(razd,2)) + " cm", font=font, fill=255)
        send.UZ(url, "/api/uz/", round(razd,2), apikey)
        
        #Pridobimo in izpišemo podatke iz DHT senzorja
        data = DHT.get_humidity() #data[0] = hum; data[1]= temp
        draw.text((x, top+16),  "TMP:" + str(data[1]) + "°C, HUM:" + str(data[0]) + "%",  font=font, fill=255)  
        send.DHT(url, "/api/dht/", data, apikey)
        
        #Pridobimo in pzpišemo podatke iz enkoderja
        counter = enkoder.getCounter()
        click = enkoder.getClick()
        draw.text((x, top+24),  "ENC:" + str(counter) + ", BUTTON:" + str(click) ,  font=font, fill=255)  


        #muska
        currentLink, playing = music.predvajaj(currentLink, playing)
        musicTitle = music.musicTitle
        draw.text((x, top+32),  "Music:" + str(musicTitle) ,  font=font, fill=255)  
        
        
        
        #Pripravljen izpis prikažemo na zaslonu
        disp.image(image)
        disp.display()
        time.sleep(0.1)

except KeyboardInterrupt:
    if DEBUG:
        print("Uporabnik je pritisnil ctrl + c.")

    #Pobrišemo informacije na zaslonu
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    font = ImageFont.load_default()
    disp.image(image)
    disp.display()

    #Ugasnemo LED strip
    for i in range(strip_len):
            
            pixels[i] = (0, 0, 0)
    #Pobrišemo nastavitve na GPIO pinih
    GPIO.cleanup()