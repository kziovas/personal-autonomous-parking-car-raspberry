from services import CarService
from sanic import Sanic
from api import car_system_controller, create_healthcheck_controller, HealthCheckController, create_car_system_controller, CarSystemController
from injector import Injector

def main_car ():
    car_controller = CarService()
    print("System initialized succesfully!")
    while True:
      car_controller.run()


def main():
  injector = Injector()
  sanic_app = Sanic("CarApp")
  
  healthcheck_controller = injector.get(HealthCheckController)
  car_system_controller = injector.get(CarSystemController)
  create_healthcheck_controller(healthcheck_controller, sanic_app)
  create_car_system_controller(car_system_controller,sanic_app)

  car_controller = injector.get(CarService)

  #sanic_app.register_listener(app.run, "before_server_start")

  sanic_app.run(host = "0.0.0.0", port = "5030", debug = True)


if __name__ == '__main__':
  main()
