import RPi.GPIO as GPIO
from time import sleep


class MotorController:
    
    def __init__(self, EnaA = 10,In1A = 3,In2A = 4, EnaB=22,In1B=17,In2B=27, EnaC=25, In1C=24, In2C=23, EnaD=14, In1D=18, In2D=15):
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        self.EnaC = EnaC
        self.In1C = In1C
        self.In2C = In2C
        self.EnaD = EnaD
        self.In1D = In1D
        self.In2D = In2D
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        GPIO.setup(self.EnaC, GPIO.OUT)
        GPIO.setup(self.In1C, GPIO.OUT)
        GPIO.setup(self.In2C, GPIO.OUT)
        GPIO.setup(self.EnaD, GPIO.OUT)
        GPIO.setup(self.In1D, GPIO.OUT)
        GPIO.setup(self.In2D, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 2*500)
        self.pwmA.start(0)
        self.pwmB = GPIO.PWM(self.EnaB, 2*500)
        self.pwmB.start(0)
        self.pwmC = GPIO.PWM(self.EnaC, 2*500)
        self.pwmC.start(0)
        self.pwmD = GPIO.PWM(self.EnaD, 2*500)
        self.pwmD.start(0)
        
    def turn_right(self, speed: float):
        speed*=100
        if speed>100:
            speed=100
        if speed<-100:
            speed=-100
        print(speed)
        
        #a and d motors
        self.pwmA.ChangeDutyCycle(abs(speed))
        GPIO.output(self.In1A, GPIO.LOW)
        GPIO.output(self.In2A, GPIO.HIGH)
        self.pwmD.ChangeDutyCycle(abs(speed))
        GPIO.output(self.In1D, GPIO.LOW)
        GPIO.output(self.In2D, GPIO.HIGH)
        #b and c motors
        self.pwmB.ChangeDutyCycle(abs(speed)) 
        GPIO.output(self.In1B, GPIO.HIGH)
        GPIO.output(self.In2B, GPIO.LOW)
        self.pwmC.ChangeDutyCycle(abs(speed)) 
        GPIO.output(self.In1C, GPIO.HIGH)
        GPIO.output(self.In2C, GPIO.LOW)
        
        

    def move(self,wheel = 'ALL',speed = 1):
        speed*=100
        if speed>100:
            speed=100
        if speed<-100:
            speed=-100

        if 'a' in wheel:
            self.pwmA.ChangeDutyCycle(abs(speed))
            if speed>0:
                GPIO.output(self.In1A, GPIO.HIGH)
                GPIO.output(self.In2A, GPIO.LOW)
            else:
                GPIO.output(self.In1A, GPIO.LOW)
                GPIO.output(self.In2A, GPIO.HIGH)
        if 'b' in wheel:
            self.pwmB.ChangeDutyCycle(abs(speed))
            if speed>0:
                GPIO.output(self.In1B, GPIO.HIGH)
                GPIO.output(self.In2B, GPIO.LOW)
            else:
                GPIO.output(self.In1B, GPIO.LOW)
                GPIO.output(self.In2B, GPIO.HIGH)
        if 'c' in wheel:
            self.pwmC.ChangeDutyCycle(abs(speed))
            if speed>0:
                GPIO.output(self.In1C, GPIO.HIGH)
                GPIO.output(self.In2C, GPIO.LOW)
            else:
                GPIO.output(self.In1C, GPIO.LOW)
                GPIO.output(self.In2C, GPIO.HIGH)
        if 'd' in wheel:
            self.pwmD.ChangeDutyCycle(abs(speed))
            if speed>0:
                GPIO.output(self.In1D, GPIO.HIGH)
                GPIO.output(self.In2D, GPIO.LOW)
            else:
                GPIO.output(self.In1D, GPIO.LOW)
                GPIO.output(self.In2D, GPIO.HIGH)
        if wheel == 'ALL':
            self.pwmA.ChangeDutyCycle(abs(speed))
            self.pwmB.ChangeDutyCycle(abs(speed))
            self.pwmC.ChangeDutyCycle(abs(speed))
            self.pwmD.ChangeDutyCycle(abs(speed))
            if speed>0:
                GPIO.output(self.In1A, GPIO.HIGH)
                GPIO.output(self.In2A, GPIO.LOW)
                GPIO.output(self.In1B, GPIO.HIGH)
                GPIO.output(self.In2B, GPIO.LOW)
                GPIO.output(self.In1C, GPIO.HIGH)
                GPIO.output(self.In2C, GPIO.LOW)
                GPIO.output(self.In1D, GPIO.HIGH)
                GPIO.output(self.In2D, GPIO.LOW)
            else:
                GPIO.output(self.In1A, GPIO.LOW)
                GPIO.output(self.In2A, GPIO.HIGH)
                GPIO.output(self.In1B, GPIO.LOW)
                GPIO.output(self.In2B, GPIO.HIGH)
                GPIO.output(self.In1C, GPIO.LOW)
                GPIO.output(self.In2C, GPIO.HIGH)
                GPIO.output(self.In1D, GPIO.LOW)
                GPIO.output(self.In2D, GPIO.HIGH)
        #self.stop()
                
    def stop(self, t=0):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        self.pwmC.ChangeDutyCycle(0)
        self.pwmD.ChangeDutyCycle(0)
        sleep(t)
     
if __name__ == '__main__':
    pass


















'''
class Motorasd():
    def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B):
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100)
        self.pwmA.start(0)
        self.pwmB = GPIO.PWM(self.EnaB, 100)
        self.pwmB.start(0)
        


    def move(self, speed=0.5, turn=0, t=0):
        speed *= 100
        turn *= 100
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        if leftSpeed > 100:
            leftSpeed = 100
        elif leftSpeed < -100:
            leftSpeed = -100
        if rightSpeed > 100:
            rightSpeed = 100
        elif rightSpeed < -100:
            rightSpeed = -100

        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))

        if leftSpeed > 0:
            GPIO.output(self.In1A, GPIO.HIGH)
            GPIO.output(self.In2A, GPIO.LOW)
        else:
            GPIO.output(self.In1A, GPIO.LOW)
            GPIO.output(self.In2A, GPIO.HIGH)

        if rightSpeed > 0:
            GPIO.output(self.In1B, GPIO.HIGH)
            GPIO.output(self.In2B, GPIO.LOW)
        else:
            GPIO.output(self.In1B, GPIO.LOW)
            GPIO.output(self.In2B, GPIO.HIGH)

        sleep(t)
        self.stop()

    def stop(self, t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);
        sleep(t)
'''