from asyncio.tasks import as_completed
import RPi.GPIO as GPIO
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from .motor_service import MotorService
from .ultrasonic_service import UltrasonicService
from .servo_service import ServoService
import keyboard as kb
from multiprocessing import Process
from utilities import blink_leds, run_cleanup
from time import sleep, time
from typing import List
from statistics import mean
from injector import inject, singleton

from services import ultrasonic_service


@singleton
class CarService:
      
    @inject
    def __init__(
        self,
        motor_service: MotorService,
        ultrasonic_service: UltrasonicService,
        servo_service: ServoService
    ) -> None:
        self.motor = motor_service
        self.servo = servo_service
        self.sensor = ultrasonic_service
        self.is_free_to_park = True
        self.retries = 3
    

    def park_if_possible(self)->bool:
        danger_lights=Process(target=blink_leds)
        danger_lights.start()
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
        danger_lights.join()
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
            while distance ==0 and retries<=self.retries :
                print(f"Number of retries: {retries}")
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
            
        if kb.is_pressed('p') and self.is_free_to_park:
            self.is_free_to_park=False
            self.park_if_possible()
            self.is_free_to_park= True
        if kb.is_pressed('s'):
            self.motor.stop()
        self.motor.stop()


    async def health_check(self)->dict:
        health_status = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            loop = asyncio.get_running_loop()
            checks = [self.motor.health_check,self.sensor.health_check,self.servo.health_check]
            for check in checks:
                future = loop.run_in_executor(executor,check)
                result = await asyncio.wait_for(future, timeout=5, loop=loop)
                health_status.update(result)


        return health_status
        
if __name__ == '__main__':
    car_controller = CarService()
    while True:
      car_controller.run()