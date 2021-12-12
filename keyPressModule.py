import keyboard


def main():
    if keyboard.is_pressed("a"):
        print('A was pressed')
    if keyboard.is_pressed('w'):
        print('W was pressed')
    if keyboard.is_pressed('s'):
        print('S was pressed')
    if keyboard.is_pressed('d'):
        print('D was pressed')
    
   
if __name__ == '__main__':
    while True:
        main()