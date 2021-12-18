from sanic.response import json, text, file
from sanic import Blueprint
from sanic import Sanic
from services import MotorService, UltrasonicService, ServoService
from injector import singleton, inject
from sanic_jinja2 import SanicJinja2

@singleton
class HealthCheckController:
    @inject
    def __init__(
        self,
        motor_service: MotorService,
        ultrasonic_service: UltrasonicService,
        servo_service: ServoService
    ):
        self.motor_service = motor_service
        self.ultrasonic_service = ultrasonic_service
        self.servo_service = servo_service

    async def get_health_status(self) -> dict:
        ultrasonic_status = self.ultrasonic_service.health_check()
        servo_status = self.servo_service.health_check()
        motors_status = self.motor_service.health_check()

        health_status ={
            "ultrasonic_sensor":ultrasonic_status,
            "servo":servo_status,
            "motors":motors_status
        }

        return health_status

def create_healthcheck_controller(
    controller: HealthCheckController,
    app: Sanic
):
    healthcheck_bp = Blueprint("healthcheck")
    jinja = SanicJinja2(app, pkg_name="main")
 
    @healthcheck_bp.route("/", methods =['GET'])
    async def index(request):

        return jinja.render("index.html", request)

    @healthcheck_bp.route("/healthcheck", methods =['GET'])
    async def get_health_status(request):
        health_status= await controller.get_health_status()

        return json(health_status)

    app.blueprint(healthcheck_bp)