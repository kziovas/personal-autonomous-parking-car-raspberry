from sanic.response import json, text, file
from sanic import Blueprint
from sanic import Sanic
from services import CarService
from injector import singleton, inject

@singleton
class CarSystemController:
    @inject
    def __init__(
        self,
        car_service: CarService
    ):
        self.car_service = car_service


def create_car_system_controller(
    controller: CarSystemController,
    app: Sanic
):
    car_system_bp = Blueprint("car_system")
    
    @car_system_bp.route("/start_car", methods =['GET'])
    async def start_car(request):
        

        return json({"car":"started"})
    
    @car_system_bp.route("/stop_car", methods =['GET'])
    async def stop_car(request):
        

        return json({"car":"stopped"})

    app.blueprint(car_system_bp)