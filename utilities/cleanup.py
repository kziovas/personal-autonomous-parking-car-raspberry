import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library


def run_cleanup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
    GPIO.cleanup()
