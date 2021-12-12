import RPi.GPIO as GPIO
import time
 

class UltrasonicController():
    def __init__(self, trigger_pin: int = 19, echo_pin: int = 13):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        

    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.trigger_pin, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(self.echo_pin) == 0:
            StartTime = time.time()
        
        # save time of arrival       
        while GPIO.input(self.echo_pin) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
     
        return distance
 
if __name__ == '__main__':
    
    sensor = UltrasonicController()
    

    try:
        while True:
            dist = sensor.distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(0.7)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

