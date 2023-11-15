import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time

centroid_x = 0  # Initialize centroid_x

def track_blob(frame):
    global centroid_x

    lower_red = np.array([0, 0, 150])
    upper_red = np.array([100, 100, 255])

    red_mask = cv2.inRange(frame, lower_red, upper_red)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
    if contours:
        max_contour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(max_contour)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        centroid_x = x + w // 2

        print('Centroid X:', centroid_x)

    return frame

broker_address = 'broker.hivemq.com'
client = mqtt.Client('sarahJackson')
client.connect(broker_address)
time.sleep(2)
client.subscribe('legoDirect')

def send_coords(xcoord):
    global centroid_x

    # Convert the coordinate to string before publishing
    client.publish('legoDirect', str(centroid_x))
    print('Message sent:', centroid_x)

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()

    result_frame = track_blob(frame)

    cv2.imshow('Red Blob Tracking', result_frame)

    send_coords(centroid_x)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()