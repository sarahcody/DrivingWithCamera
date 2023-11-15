# DrivingWithCamera
Overall, the purpose of this code is to 

## Real-time Blob Tracking with MQTT Integration: legoCarCode.py
This Python script captures video from a camera, tracks a red blob in the frames, and publishes the x-coordinate of the blob's centroid using the MQTT (Message Queuing Telemetry Transport) protocol.

### Prerequisites
Python 3.x
OpenCV (cv2) library
NumPy (numpy) library
Paho MQTT (paho-mqtt) library


## Pico IoT Communication Example: 
This Python script demonstrates a simple Internet of Things (IoT) application using the Raspberry Pi Pico microcontroller. The script combines Wi-Fi, MQTT (Message Queuing Telemetry Transport), and Bluetooth Low Energy (BLE) communication to exchange data with remote devices.

Features
Wi-Fi Connectivity: Connects to a Wi-Fi network using the specified SSID and password.
MQTT Communication: Subscribes to an MQTT topic (legoDirect) to receive messages and prints them.
Bluetooth Low Energy (BLE): Sends data over BLE to a peripheral device and prints received data.
Prerequisites
MicroPython Environment: Ensure that your Raspberry Pi Pico is set up with MicroPython.
Wi-Fi Credentials: Update the wifi dictionary with the SSID and password of your Wi-Fi network.
MQTT Broker: Modify the mqtt_broker variable to the address of your MQTT broker.
Bluetooth Name: Set the bluetooth_name variable to the desired name for your Bluetooth device.
