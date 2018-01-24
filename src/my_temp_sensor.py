import dht11
import time
import datetime
import RPi.GPIO as GPIO

def main():
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    # read data using pin 14
    instance = dht11.DHT11(pin=4)
    while True:
        result = instance.read()
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature is: %d degree centigrade" % result.temperature)
            print("Humidity is: %d percent" % result.humidity)
        time.sleep(3)

def getCurrent():
    currSet = {}
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    #global currSet
    #print('gpio setup initiated')
  
    # read data using pin 14
    instance = dht11.DHT11(4)
    i = 0
    while i < 10:
        result = instance.read()
        if result.is_valid():
            print("Time: " + str(datetime.datetime.now()))
            print("Temperature is: %d degree centigrade" % result.temperature)
            print("Humidity is: %d percent" % result.humidity)
            currSet['humidity'] = result.humidity
            currSet['temp'] = result.temperature
            break
        elif i == 9 and result.is_valid() == False :
            currSet['humidity'] = 'na'
            currSet['temp'] = 'na'          
        time.sleep(1)    
        i = i+1
    
    return currSet
    

if __name__ == '__main__':
    main()