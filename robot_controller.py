import RPi.GPIO as GPIO
from MotorModule import Motor
import keyboard as kb
import subprocess
from time import sleep, time
from typing import List
import ultrasonic as us
from statistics import mean
import servo_scan as scan


class RobotController:
    RETRIES = 3
    GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)

    def __init__(self) -> None:
        self.motor = Motor()
        self.servo = scan.ServoController()
        self.sensor = us.UltrasonicController()  



    def park_if_possible():
        danger_lights=subprocess.Popen(['python', 'led.py'])
        distances = scan_spot()

        if is_spot_aceptable(distances):
            print("Parking...")
            #move_in_spot()
            print("Parking complete")
            
        else:
            print("This spot is not large enough!\nLets keep looking!")
        
        sleep(2)
        danger_lights.terminate()
        GPIO.output(2, GPIO.LOW)


    def is_spot_aceptable(distances: List[int]) -> bool:

        if any(x<25 for x in distances):
            return False
        else:
            return True


    def move_in_spot():
        end_time = time()+0.6

        while time() < end_time:
            move_car("right", speed=0.3)
            sleep(0.1)

        move_car("stop")


   
    def scan_spot():
        distances = []
        for i in range(10,1,-2):
            self.servo.look(angle=i)
            measurements = []
            distance = 0
            retries = 0
            while distance ==0 and retries<=self.RETRIES :
                print(retries)
                retries += 1
                for _ in range(1,10):
                    sleep(0.05)
                    measurements.append(sensor.distance())
                    sleep(0.05)

                #Filter extreme values from measurements
                filtered_measurements = [x  for x in measurements if x <(1.5*mean(measurements)) and x > mean(measurements)/1.5]
                if len(filtered_measurements) >0:
                    distance = mean(filtered_measurements)
                else:
                    distance = 0
        

            distances.append(distance)
            print(distance)

        self.servo.look("middle")
        print(distances)
        return distances

    def move_car(direction: str = None, speed:float = 0.7):

        #forward
        if direction == "forward":
            self.motor.move(wheel='ALL',speed=speed)
            print("forward")
        
        #backward
        elif direction == "backward":
            self.motor.move(wheel='ALL',speed=-speed)
            print("back")

        #left
        elif direction == "left":
            self.motor.move('a',speed=-speed)
            self.motor.move('b',speed=speed)
            self.motor.move('c',speed=-speed)
            self.motor.move('d',speed=speed)
            print("left")

        #right
        elif direction == "right":
            self.motor.move('a',speed=speed)
            self.motor.move('b',speed=-speed)
            self.motor.move('c',speed=speed)
            self.motor.move('d',speed=-speed)
    
            print("right")

        #left-forward
        elif direction == "left-forward":
            self.motor.move(wheel='a',speed=-speed)
            self.motor.move(wheel='c',speed=-speed) 
            print("left-forward")

        #left-backward
        elif direction == "left-backward":
            self.motor.move(wheel='b',speed=speed)
            self.motor.move(wheel='d',speed=speed)
            print("left-backward")

        #right-forward
        elif direction == "right-forward":
            self.motor.move(wheel='b',speed=-speed)
            self.motor.move(wheel='d',speed=-speed)
            print("right-forward")

        #right-backward
        elif direction == "right-backward":
            self.motor.move(wheel='a',speed=speed)
            self.motor.move(wheel='c',speed=speed)
            print("right-backward")
        
        #rotate-clockwise
        elif direction == "rotate-clockwise":
            self.motor.move('ad',speed=speed)
            self.motor.move('bc',speed=-speed)
            print("rotate-clockwise")
        
        #rotate-anticlockwise
        elif direction == "rotate-anticlockwise":
            self.motor.move('ad',speed=-speed)
            self.motor.move('bc',speed=speed)
            print("rotate-anticlockwise")
        
        elif direction == "stop":
            self.motor.stop()
            print("motors stoped")
        
        else:
            print("invalid-direction")
            self.motor.stop()
        



    def run():
        
        #MOVE FORWORD / BACKWORDS
        if kb.keyboard.is_pressed('x'):
            move_car("forward")
        elif kb.keyboard.is_pressed('w'):
            move_car("backward")
        
        #MOVE SIDEWAYS    
        elif kb.keyboard.is_pressed('a'):
            move_car("left")
        elif kb.keyboard.is_pressed('d'):
            move_car("right")
        
        #MOVE DIAGONALLY    
        elif kb.keyboard.is_pressed('q'):
            move_car("left-forward")
        elif kb.keyboard.is_pressed('e'):
            move_car("right-forward")
        elif kb.keyboard.is_pressed('z'):
            move_car("left-backward")
        elif kb.keyboard.is_pressed('c'):
            move_car("right-backward")
        #ROTATE    
        elif kb.keyboard.is_pressed('k'):
            move_car("rotate-clockwise")
        elif kb.keyboard.is_pressed('l'):
            move_car("rotate-anticlockwise")
        else:
            pass
            
        if kb.keyboard.is_pressed('p'):
            park_if_possible()
        if kb.keyboard.is_pressed('KP0'):
            self.motor.stop()
        self.motor.stop()
        
if __name__ == '__main__':
        
    while True:
      robot = RobotController()
      robot.run()