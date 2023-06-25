import random
import time

import requests
from paho.mqtt import client as mqtt_client

"""
TODO:
-encrypted storage of username & password
-communication with cloud
-deconstruction of data frame and sending it to the plc
-non blocking communication with cloud
"""

# Define the URL of the endpoint
url = 'http://16.16.220.162:8080/your-endpoint'  # cloud
# url = 'http://127.0.0.1:8080/your-endpoint'    # on-premise
# Define the data to send in the request body

broker = '192.168.1.100'
port = 1883
topic = "connection_001/from_plc/siemens_001"
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'simatic'
password = 'SecureConnection'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker <{broker}>, client_id: <{client_id}> listening to <{topic}>")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        # mess = [float(part) for part in msg.payload.decode().split()]
        # print("Message content: " + str(msg.payload.decode()))
        # publish(client, "other_topic", msg.payload.decode())

        data = {
            'value': 15
        }
        response = requests.post(url, json=data)
        # Check the response status code
        if response.status_code == 200:
            # Request was successful
            result = response.json()
            print('Result:', result)
            publish(client, "connection_001/to_plc/cloud_001", str(result))
        else:
            # Request encountered an error
            print('Error:', response.status_code, response.json())

    client.subscribe(topic)
    client.on_message = on_message


def publish(client: mqtt_client, topic: str, message: str):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print("Message published successfully!")
    else:
        print("Failed to publish message")


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
