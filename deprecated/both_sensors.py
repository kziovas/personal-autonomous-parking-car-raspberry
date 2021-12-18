from gpiozero import DistanceSensor
import RPi.GPIO as GPIO
from time import sleep
from services import Motor
import subprocess
from subprocess import check_call


motor = Motor()
sensor = DistanceSensor(echo=26, trigger=19)

GPIO.setmode(GPIO.BCM)
count=0   
# The input pin which is connected with the sensor
GPIO_PIN = 21
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
global c


def outputFunction(null):
        global count
        count=count+1 
        return count
# signal detection (raising edge).
GPIO.add_event_detect(GPIO_PIN, GPIO.RISING, callback=outputFunction, bouncetime=100)



def funct():
    c= 0
    apostasi = round(sensor.distance*100)
    if apostasi < 10 :
        print ("motor move", count)
        motor.move(wheel='ALL',speed=0.16)      
    elif apostasi > 25 and count > (count-20) and count > 15:
        print ("it fits  ", count)
        motor.move(wheel='ALL',speed=0.16)
        motor.stop()
        p=subprocess.Popen(['python', 'photo_sensor.py'])
        check_call(["pkill", "-f", "both_sensors.py"])
        #exit()
    else:
        print ("panw apo 10    ", count)
        motor.move(wheel='ALL',speed=0.16)

while True:
    funct()
    
