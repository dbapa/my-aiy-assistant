import dht11
import time
import datetime
import RPi.GPIO as GPIO
import my_locker as locker

# Read the Voice Hat BCM pin from the locker
VOICE_HAT_PIN = int(locker.getContent("gpio","dht_bcm_pin"))

def main():
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    # read data using pin 14
    # pin-4: (BCM 0 Driver 0 on Voice HAT)
    # pin-17: (BCM 17 Driver 1 on Voice HAT)
    # pin-27: (BCM 27 Driver 2 on Voice HAT)
    # pin-22: (BCM 22 Driver 3 on Voice HAT)
    # pin-26: (BCM 26 Servo 0 on Voice HAT) - to be used in current config
    

    instance = dht11.DHT11(VOICE_HAT_PIN)
    # print ("PIN set in instance is:",instance._DHT11__pin)
    # print (type(instance._DHT11__pin))
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
    instance = dht11.DHT11(pin=VOICE_HAT_PIN)
    
    i = 0
    '''
    Will make 10 attempts to read the temp from the sensor. This is  
    required compensate for any errors in reading sensor data due to 
    any delays in code execution (hardware I/O better in C)
    '''
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
