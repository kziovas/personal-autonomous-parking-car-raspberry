from controllers import CarController

def main ():
    car_controller = CarController()
    print("System initialized succesfully!")
    while True:
      car_controller.run()


if __name__ == '__main__':
        main()
