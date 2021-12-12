import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module


def blink_leds():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
    GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)

    try:
        while True:
            GPIO.output(2, GPIO.HIGH) # Turn on
            sleep(0.5) # Sleep for 1 second
            GPIO.output(2, GPIO.LOW) # Turn off
            sleep(0.5) # Sleep for 1 second
    
    except KeyboardInterrupt:
        
        print("Exit pressed Ctrl+C")

    finally:
        GPIO.cleanup()
        print("End of programm")