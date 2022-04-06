import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT11

def setDHT_pin(dht_pin):
    global DHT_PIN
    DHT_PIN = dht_pin

def get_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return(humidity, temperature)
    else:
        return("no data humidity", "no data temperature")
