import random
import time

import requests
from paho.mqtt import client as mqtt_client

"""
TODO:
-encrypted storage of username & password
-mpc
-adrc
"""

# Define the URL of the endpoint
# url = 'http://16.16.220.162:8080/cloud-controller-endpoint'  # cloud
url = 'http://127.0.0.1:8080/cloud-controller-endpoint'    # on-premise
# Define the data to send in the request body

broker = '192.168.1.100'
port = 1883
topic = "connection_001/from_plc/siemens_001"
cloud_topic = "connection_001/to_plc/cloud_001"
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


def system_model(y, u):
    delta_y = (-1 / T) * y + (K / T) * u
    y = y + delta_y * H
    return y

K = 0.925156  # Gain
T = 3.45  # Time constant
T0 = 0.1  # Dead time
H = 0.1  # Sampling time

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        mess = [float(part) for part in msg.payload.decode().split()]
        print(mess)
        if len(mess) > 0:
            data = {
                'SetPoint': mess[0],
                'ProcessVariable': mess[1],
                'ControlVariable': mess[2],
                'ErrorSum': mess[3],
                'ControllerType': 'MPC'
            }
            # print(f"pv = {mess[1]}, sim_pv = {system_model(mess[1], mess[2])}")
            try:
                time1 = time.perf_counter_ns()
                response = requests.post(url, json=data, timeout=0.09)
                time2 = (time.perf_counter_ns() - time1)/1000000
                print(f"time elapsed: {time2} ms")
                # Check the response status code
                if response.status_code == 200:
                    # Request was successful
                    result = response.json()
                    print('Result:', result)
                    output = result['result']
                    publish(client, cloud_topic, str(random.randint(100000, 999999))+"{0:.6f}".format(float(output))[:6])
                else:
                    print('Error:', response.status_code, response.json())
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print("Error while sending data to Cloud - server not responding! (trying again)")

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
    client = None
    while client is None:
        try:
            client = connect_mqtt()
            subscribe(client)
        except ConnectionRefusedError:
            print("MQTT Broker unavailable - trying again")
        else:
            client.loop_forever()


if __name__ == '__main__':
    run()
