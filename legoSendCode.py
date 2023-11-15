import time
import struct
import ubinascii
import network
import mqtt  # Assuming you have a custom mqtt module or import it from the MicroPython library
import bluetooth

NAME_FLAG = 0x09
ADV_TYPE_UUID128_COMPLETE = 0x07
IRQ_CENTRAL_CONNECT = 1
IRQ_CENTRAL_DISCONNECT = 2
IRQ_GATTS_WRITE = 3

UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

FLAG_READ = 0x0002
FLAG_WRITE_NO_RESPONSE = 0x0004
FLAG_WRITE = 0x0008
FLAG_NOTIFY = 0x0010

UART_UUID = UART_SERVICE_UUID
UART_TX = (UART_TX_CHAR_UUID, FLAG_READ | FLAG_NOTIFY,)
UART_RX = (UART_RX_CHAR_UUID, FLAG_WRITE | FLAG_WRITE_NO_RESPONSE,)
UART_SERVICE = (UART_UUID, (UART_TX, UART_RX),)

wifi = {"ssid": "Tufts_Wireless", "pass": ""}


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


class Yell:  # peripheral
    def __init__(self):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        # register a UART service
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((UART_SERVICE,))
        services = [UART_UUID]
        print('setup as uart')
        self._connections = set()
        self._write_callback = None
        self._first_message_received = False
        self._ble.irq(self._irq)
        self._write_callback = self.on_rx

    def advertise(self, name='Sarah', interval_us=100000):
        short = name[:8]
        payload = struct.pack("BB", len(short) + 1, NAME_FLAG) + short  # byte length, byte type, value
        value = bytes(UART_UUID)
        payload += struct.pack("BB", len(value) + 1, ADV_TYPE_UUID128_COMPLETE) + value

        self._ble.gap_advertise(interval_us, adv_data=payload)

    def stop_advertising(self):
        if not self._first_message_received:
            self._ble.gap_advertise(None)

    def _irq(self, event, data):  # Track connections so we can send notifications.
        if event == IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)
            self.stop_advertising()  # only have one connection

        elif event == IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            self._write_callback = None
            # Start advertising again to allow a new connection.
            # self._advertise()

        elif event == IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)

    def on_rx(self, v):
        print("received ", v)
        self._first_message_received = True  # Stop advertising only after the first message is received
        self.send(v)

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)

    def is_connected(self):
        return len(self._connections) > 0

    def disconnect(self):
        for conn_handle in self._connections:
            self._ble.gap_disconnect(conn_handle)


if __name__ == "__main__":
    # Initialize and connect to Wi-Fi
    connect_wifi(wifi)

    # Initialize the Yell class for Bluetooth communication
    p = Yell()
    p.advertise('Fred')

    # Wait for a Bluetooth connection
    while not p.is_connected():
        time.sleep(0.5)

    # Stop advertising after the first message is received
    p.stop_advertising()

    # Define the MQTT callback function
    def whenCalled(topic, msg):
        # Decode the message received from MQTT
        direction = msg.decode()
        print(direction)
        p.send(direction)

    # Set up the MQTT client
    fred = mqtt.MQTTClient('Sarah', '10.243.85.48', port=1885, rkeepalive=60)
    print('Connected')
    fred.connect()
    fred.set_callback(whenCalled)
    fred.subscribe(b'legoDirect')

    # Keep checking for MQTT messages
    try:
        while True:
            fred.check_msg()
            time.sleep(0.01)
    except Exception as e:
        print(e)
    finally:
        # Disconnect from MQTT and Bluetooth
        fred.disconnect()
        p.disconnect()
        print('Done')
