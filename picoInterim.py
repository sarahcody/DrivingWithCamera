import network
import time
import network
import time
import struct
import ubinascii
from mqtt import MQTTClient
from BLE_CEEO import Yell
import uasyncio as asyncio

wifi = {"ssid": "Tufts_Wireless", "pass": ""}
mqtt_broker = "broker.hivemq.com"
mqtt_topic = b"legoDirect"
bluetooth_name = "jackson"

def connect_wifi(wifi):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    print("MAC " + mac)

    station.connect(wifi['ssid'], wifi['pass'])
    while not station.isconnected():
        time.sleep(1)
    print('Connection successful')
    print(station.ifconfig())

async def mqtt_task():
    fred = MQTTClient('MyPico', mqtt_broker, keepalive=1000)
    fred.set_callback(on_message)
    fred.connect()
    fred.subscribe(mqtt_topic)

    try:
        while True:
            await asyncio.sleep(0.1)
            fred.check_msg()
    finally:
        fred.disconnect()

async def bluetooth_task():
    p = None
    try:
        p = Yell(bluetooth_name, verbose=False)
        if p.connect_up():
            print('Peripheral connected')
            await asyncio.sleep(2)

            for i in range(100):
                payload = str(i)
                p.send(payload)
                if p.is_any:
                    print(p.read())
                if not p.is_connected:
                    print('Lost connection')
                    break
                await asyncio.sleep(0.1)
    except Exception as e:
        print(e)
    finally:
        if p:
            p.disconnect()
            print('Closing up')

async def main():
    connect_wifi(wifi)
    tasks = [mqtt_task(), bluetooth_task()]
    await asyncio.gather(*tasks)

asyncio.run(main())
