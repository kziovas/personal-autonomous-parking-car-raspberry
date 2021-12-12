import RPi.GPIO as GPIO
from .motor_controller import MotorController
from .ultrasonic_controller import UltrasonicController
from .servo_controller import ServoController
import keyboard as kb
import subprocess
from utilities import blink_leds, run_cleanup
from time import sleep, time
from typing import List
from statistics import mean



class CarController:
    RETRIES = 3
  

    def __init__(self) -> None:
        run_cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
         # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(2, GPIO.OUT, initial=GPIO.LOW) 
        self.motor = MotorController()
        self.servo = ServoController()
        self.sensor = UltrasonicController()  



    def park_if_possible(self)->bool:
        danger_lights=subprocess.Popen(blink_leds)
        distances = self.scan_spot()
        is_parked = False

        if self.is_spot_aceptable(distances):
            print("Parking...")
            #move_in_spot()
            print("Parking complete")
            is_parked= True
            
        else:
            print("This spot is not large enough!\nLets keep looking!")

        
        sleep(2)
        danger_lights.terminate()
        GPIO.output(2, GPIO.LOW)
        return is_parked


    def is_spot_aceptable(self,distances: List[int]) -> bool:

        if any(x<25 for x in distances):
            return False
        else:
            return True


    def move_in_spot(self)->None:
        end_time = time()+0.6

        while time() < end_time:
            self.move_car("right", speed=0.3)
            sleep(0.1)

        self.move_car("stop")


   
    def scan_spot(self) -> list:
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
                    measurements.append(self.sensor.distance())
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

    def move_car(self,direction: str = None, speed:float = 0.7) -> None:

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
        



    def run(self)->None:
        
        #MOVE FORWORD / BACKWORDS
        if kb.is_pressed('x'):
            self.move_car("forward")
        elif kb.is_pressed('w'):
            self.move_car("backward")
        
        #MOVE SIDEWAYS    
        elif kb.is_pressed('a'):
            self.move_car("left")
        elif kb.is_pressed('d'):
            self.move_car("right")
        
        #MOVE DIAGONALLY    
        elif kb.is_pressed('q'):
            self.move_car("left-forward")
        elif kb.is_pressed('e'):
            self.move_car("right-forward")
        elif kb.is_pressed('z'):
            self.move_car("left-backward")
        elif kb.is_pressed('c'):
            self.move_car("right-backward")
        #ROTATE    
        elif kb.is_pressed('k'):
            self.move_car("rotate-clockwise")
        elif kb.is_pressed('l'):
            self.move_car("rotate-anticlockwise")
        else:
            pass
            
        if kb.is_pressed('p'):
            self.park_if_possible()
        if kb.is_pressed('s'):
            self.motor.stop()
        self.motor.stop()
        
if __name__ == '__main__':
        
    while True:
      car_controller = CarController()
      car_controller.run()