import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import asyncio
from time import sleep
from injector import inject, singleton # Import the sleep function from the time module

@singleton
class LEDUtil:
    @inject
    def __init__(self) -> None:
        self._led_working = False

    def blink_leds(self)-> bool:
        GPIO.setwarnings(False) # Ignore warning for now
        #GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
        GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
        #print("led blinking started")
        try:
            self._led_working = True
            while self._led_working:
                GPIO.output(2, GPIO.HIGH) # Turn on
                sleep(0.4) # Sleep for 1 second
                GPIO.output(2, GPIO.LOW) # Turn off
                sleep(0.4) # Sleep for 1 second
            GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW)
            GPIO.cleanup()
            print("End of programm")
            return True
        
        except Exception as exc:
            raise exc

    def stop_leds(self):
        self._led_working = False