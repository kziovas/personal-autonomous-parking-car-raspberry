from sanic.response import json, text, file
from sanic import Blueprint
from sanic import Sanic
from services import CarService
from injector import singleton, inject
from sanic_jinja2 import SanicJinja2

from services.car_service import CarService

@singleton
class HealthCheckController:
    @inject
    def __init__(
        self,
        car_service: CarService
    ):
        self.car_service = car_service

    async def get_health_status(self) -> dict:
        health_status= await self.car_service.health_check()

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