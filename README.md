# DrivingWithCamera
Overall, the purpose of this code is to 

## Real-time Blob Tracking with MQTT Integration: camera_test.py
This Python script captures video from a camera, tracks a red blob in the frames, and publishes the x-coordinate of the blob's centroid using the MQTT (Message Queuing Telemetry Transport) protocol.

### Prerequisites
1. Python 3.x
2. OpenCV (cv2) library
3. NumPy (numpy) library
4. Paho MQTT (paho-mqtt) library

### Configuration
1. Adjust the lower_red and upper_red values in the script to match the color range of your specific blob.
2. Modify the broker_address variable to the address of your MQTT broker.

### MQTT Integration
The script connects to an MQTT broker at broker.hivemq.com using the client ID 'sarahJackson' and subscribes to the topic 'legoDirect'. It publishes the x-coordinate of the tracked blob's centroid to the same 'legoDirect' topic

## Raspberry Pi Pico IoT Communication: picoInterim.py
This Python script showcases an IoT application using the Raspberry Pi Pico microcontroller, integrating Wi-Fi, MQTT, and Bluetooth Low-Energy (BLE) communication. It establishes a connection to a Wi-Fi network, subscribes to an MQTT topic, and exchanges data with a BLE peripheral device.

### Features
1. Wi-Fi Connectivity: Connects to a Wi-Fi network using the specified SSID and password.
2. MQTT Communication: Subscribes to the MQTT topic legoDirect to receive and print messages.
3. Bluetooth Low Energy (BLE): Initiates communication with a BLE peripheral device named "jackson" and exchanges data.

### Prerequisites
1. MicroPython Environment: Ensure your Raspberry Pi Pico is set up with MicroPython.
2. Wi-Fi Credentials: Update the wifi dictionary with your Wi-Fi SSID and password.
3. MQTT Broker: Set the mqtt_broker variable to the address of your MQTT broker.
4. Bluetooth Name: Adjust the bluetooth_name variable as needed.
Installation
5. Copy the script to your Raspberry Pi Pico or the storage device used for flashing.
6. Make sure the required libraries (mqtt, BLE_CEEO, uasyncio) are available in your MicroPython environment.

### Usage
1. Power on your Raspberry Pi Pico.
2. The script will automatically connect to Wi-Fi, subscribe to MQTT, and initiate BLE communication.
3. Monitor the console for Wi-Fi connection status, MQTT messages, and BLE communication updates.

### Configuration
Customize the wifi, mqtt_broker, and bluetooth_name variables in the script to match your specific setup.
Contributing
Contributions are welcome! If you encounter issues or have improvements, please open an issue or create a pull request.


## Bluetooth-controlled Car: legoCarCode.py
This Python script demonstrates the use of the BLE_CEEO library to control a car wirelessly via Bluetooth Low Energy (BLE). The car is controlled based on the values received from a BLE peripheral device.

### Features
1. Bluetooth Connection: Connects to a BLE peripheral device with the name "sarahJacksonCar."
2. Car Control: Interprets incoming data to control the car's movement (forward, backward, turn right, turn left).

### Prerequisites
1. BLE Peripheral Device: Ensure there is a BLE peripheral device with the name "sarahJacksonCar" that can send data.
2. BLE_CEEO Library: Make sure the BLE_CEEO library is installed in your Python environment.

### Usage
1. Ensure the BLE peripheral device is turned on and discoverable.

### Data Interpretation
The script interprets incoming data as follows:

0 to 63: Move the car forward.  

64 to 127: Move the car backward.  

128 to 191: Turn the car right.  

192 to 255: Turn the car left.  

Invalid values or non-numeric data will be reported as errors.


