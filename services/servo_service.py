import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
from .ultrasonic_service import UltrasonicService 
from utilities import HealthStatus
from injector import singleton



@singleton
class ServoService():
    
    def __init__(self, pin: int = 26, cycle_start: float = 3, cycle_step: float = 3,
                 cycle_end: float = 9, rest_position: float = 6, pwm_freq: float = 50):
        self.cycle_start = cycle_start
        self.cycle_step = cycle_step
        self.cycle_end = cycle_end
        self.rest_position = rest_position
        self.pwm_freq = pwm_freq
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        self.pwm = GPIO.PWM(pin,pwm_freq)
        self.sensor = UltrasonicService()
        self.pwm.start(0)
        
        
    def run_scan(self):
        self.pwm.start(0)
        duty_cycle = self.cycle_start
        Retdistances = []
        while duty_cycle <= self.cycle_end:
            distances = []
            self.pwm.ChangeDutyCycle(duty_cycle)
            
            print(duty_cycle)
            duty_cycle +=  self.cycle_step
            for i in range(10):
                distance = self.sensor.distance()
                if distance > 0.5:
                    distances.append(distance)
            Retdistances.append(sum(distances)/len(distances))
            sleep(2)
        self.pwm.ChangeDutyCycle(self.rest_position)
        sleep(0.5)
        self.pwm.ChangeDutyCycle(0)
        
        print(Retdistances)
        return Retdistances
    
    def look(self, direction:str = "middle", angle:int = None):
        if angle is None:
            if direction == "ahead":
                self.pwm.ChangeDutyCycle(self.cycle_end)
                sleep(0.5)
                self.pwm.ChangeDutyCycle(0)
            elif direction == "back":
                self.pwm.ChangeDutyCycle(self.cycle_start)
                sleep(0.5)
                self.pwm.ChangeDutyCycle(0)
            else:
                self.pwm.ChangeDutyCycle(self.rest_position)
                sleep(0.5)
                self.pwm.ChangeDutyCycle(0)
        elif angle >= 2 and angle <=10 :
                self.pwm.ChangeDutyCycle(angle)
                sleep(0.5)
                self.pwm.ChangeDutyCycle(0)
        else:
            self.pwm.ChangeDutyCycle(self.rest_position)
            sleep(0.5)
            self.pwm.ChangeDutyCycle(0)
            print("Invalid angle provided for servo!")
            print("Angles should be from 3 to 9")

    def health_check(self) -> str:
        try:
            self.run_scan()
            status = HealthStatus.HEALTHY.value
        except Exception as exc:
            status = HealthStatus.UNHEATLHY.value
        finally:
            return status

    
       
        


if __name__ == "__main__":

    servo = ServoService()
    servo.run_scan()

