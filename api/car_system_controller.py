import asyncio
import subprocess
import json
from asyncio.events import AbstractEventLoop
from typing import AsyncContextManager
from sanic.response import json, text, file
from sanic import Blueprint
from sanic import Sanic
from services import CarService
from injector import singleton, inject
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus
from multiprocessing import Process
from os.path import dirname
from os import path

@singleton
class CarSystemController:
    @inject
    def __init__(
        self,
        car_service: CarService
    ):
        self.car_service = car_service
        self.car_task =None
        self.loop: AbstractEventLoop
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.main_path = dirname(dirname(__file__))

    async def start_car(self):
        try:
            if not self.car_task:
                #self.loop = asyncio.get_event_loop()
                #self.car_task =  self.loop.run_in_executor(self.executor, self.car_service.run)
                self.car_task = asyncio.create_task(self.car_service.run())
            
            return HTTPStatus.OK

        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
        

    async def stop_car(self):
        try:
            if self.car_task:
                self.car_service.stop()
                await self.car_task
                self.car_task =None

            return HTTPStatus.OK

        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR


def create_car_system_controller(
    controller: CarSystemController,
    app: Sanic
):
    car_system_bp = Blueprint("car_system")
    car_system_controller = controller
    
    @car_system_bp.route("/start_car", methods =['GET'])
    async def start_car(request):
        response = await car_system_controller.start_car()

        return json({"start_car":str(response)})
    
    @car_system_bp.route("/stop_car", methods =['GET'])
    async def stop_car(request):
        response = await car_system_controller.stop_car()

        return json({"stop_car":str(response)})

    app.blueprint(car_system_bp)