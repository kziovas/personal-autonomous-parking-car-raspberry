# Needed modules will be imported and configured 
import RPi.GPIO as GPIO
import time
from services.motor_service import Motor
import subprocess
from subprocess import check_call
  
GPIO.setmode(GPIO.BCM)
count=0   
# The input pin which is connected with the sensor
GPIO_PIN = 21
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
 
#print ("KY-010 Sensor Test [press ctrl+c to end the test]")
motor = Motor()

def outputFunction(null):
        global count
        count=count+1 
        #print("Sensor is blocked",count)
        return count
# signal detection (raising edge).
GPIO.add_event_detect(GPIO_PIN, GPIO.RISING, callback=outputFunction, bouncetime=100) 

# Main program loop
try:
        while True:
                time.sleep(0.3)
                motor.move(wheel='ALL',speed=-0.19)
                print(count)
                if count > 10:
                    motor.stop()
                    print("back_stop")
                    p=subprocess.Popen(['python', 'final_parking.py'])
                    check_call(["pkill", "-f", "photo_sensor.py"])
                    #exit()
  
# Scavenging work after the end of the program
except KeyboardInterrupt:
        print("Total count", count)
        GPIO.cleanup()
