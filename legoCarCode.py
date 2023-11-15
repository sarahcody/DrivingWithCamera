from BLE_CEEO import Yell

bluetooth_name = "sarahJacksonCar"

def move_car(data):
    try:
        value = int(data)
        if 0 <= value <= 63:
            # Move forward
            print('Moving forward')
        elif 64 <= value <= 127:
            # Move backward
            print('Moving backward')
        elif 128 <= value <= 191:
            # Turn right
            print('Turning right')
        elif 192 <= value <= 255:
            # Turn left
            print('Turning left')
        else:
            print('Invalid value received:', value)
    except ValueError:
        print('Invalid data received:', data)

def main():
    p = None
    try:
        p = Yell(bluetooth_name, verbose=False)
        if p.connect_up():
            print('Peripheral connected')

            while True:
                if p.is_any:
                    received_data = p.read()
                    move_car(received_data)
    except Exception as e:
        print(e)
    finally:
        if p:
            p.disconnect()
            print('Closing up')


main()
