from services import MotorService, UltrasonicService, ServoService
from injector import provider, Module, singleton

class CoreModule(Module):

    @singleton
    @provider
    def create_motor_service(self)->MotorService:
        motor = MotorService()
        return motor

    @singleton
    @provider
    def create_sensor_service(self)->UltrasonicService:
        sensor = UltrasonicService(trigger_pin=19, echo_pin=13)
        return sensor

    @singleton
    @provider
    def create_servo_service(self)->ServoService:
        servo = ServoService()
        return servo