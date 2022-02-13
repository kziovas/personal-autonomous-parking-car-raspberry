import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import asyncio
from time import sleep
from injector import inject, singleton # Import the sleep function from the time module

@singleton
class LEDUtil:
    @inject
    def __init__(self) -> None:
        self._led_working = False

    def aborting_led(self)-> bool:
        GPIO.setwarnings(False) # Ignore warning for now
        #xwpwwxxGPIO.setmode(GPIO.BCM) # Use BCM pin numbering
        GPIO.setup(20, GPIO.OUT, initial=GPIO.LOW) # Set pin 20 to be an output pin and set initial value to low (off)
        try:
            for _ in range(4):
                GPIO.output(20, GPIO.HIGH) # Turn on
                sleep(0.4) # Sleep for 1 second
                GPIO.output(20, GPIO.LOW) # Turn off
                sleep(0.4) # Sleep for 1 second
            GPIO.setup(20, GPIO.OUT, initial=GPIO.LOW)
            return True

        except Exception as exc:
            raise exc



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
            print("End of programm")
            return True
        
        except Exception as exc:
            raise exc

    def stop_leds(self):
        self._led_working = False

if __name__ == '__main__':
    led_Service = LEDUtil()
    led_Service.aborting_led()