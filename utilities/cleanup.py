import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library


def run_cleanup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.cleanup()
