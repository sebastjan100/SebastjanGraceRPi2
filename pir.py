import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
from settings import *

GPIO.setmode(GPIO.BCM)

last_move = None

def initialize(pir):
        GPIO.setup(pir, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

#define functions which will be triggered on pin state changes
def pirMove(pir):
        def pirInterupt(channel):
                global last_move
                print("Premik")
                last_move = time.time()
        return pirInterupt

def getLastMove():
  global last_move
        return last_move

if __name__ == "__main__":
        pir = 13
        initialize(pir)
        try:
                GPIO.add_event_detect(pir, GPIO.FALLING, callback=pirMove(pir), bouncetime=100)
                input("Test pir\n")
        except KeyboardInterrupt:
                print("Ctl C pressed - ending program")

# GPIO.cleanup() # resets GPIO ports used back to input mode