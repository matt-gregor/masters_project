import csv
import os
import random
import signal
import time

import requests
from dotenv import find_dotenv, load_dotenv
from paho.mqtt import MQTTException
from paho.mqtt import client as mqtt_client

# Define the URL of the endpoint
url = 'http://16.16.220.162:8080/cloud-controller-endpoint'  # cloud
# url = 'http://127.0.0.1:8080/cloud-controller-endpoint'    # on-premise (testing)

# Connection data
broker = '192.168.1.100'
port = 1883
topic = "connection_001/from_plc/siemens_001"
cloud_topic = "connection_001/to_plc/cloud_001"
client_id = f'python-mqtt-{random.randint(0, 100)}'
time_sum = 0.0
average = 0.0
msg_count = 0
previous_controller_type = ''
session = None
f = None
path = 'C:\\Projekty\\mgr\\measurements\\measurements1.csv'

def load_vulnerable_data():
    load_dotenv(find_dotenv())


def close_file(signal_num, frame):
    global f
    if f:
        f.close()
    print("Program interrupted by Ctrl + C.")
    exit(0)


signal.signal(signal.SIGINT, close_file)


if os.path.exists(path):
    f = open(path, 'a', newline='')
    writer = csv.writer(f)
else:
    f = open(path, 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(['set_point',
                     'process_variable',
                     'control_variable',
                     'controller_type',
                     'current_error',
                     'overshoot',
                     'regulation_time',
                     'rise_time',
                     'ISE',
                     'IAE',
                     'MSE',
                     'control_cost',
                     'plc_control_variable',
                     'gateway_time_elapsed',
                     'server_time_elapsed'])


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker <{broker}>, client_id: <{client_id}> listening to <{topic}>")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global time_sum, average, msg_count, previous_controller_type
        raw_mess = msg.payload.decode().split()
        if raw_mess:
            mess = [float(part) for part in raw_mess[:-1]]
            mess.append(raw_mess[-1].upper())
            data = {
                'SetPoint': mess[0],
                'ProcessVariable': mess[1],
                'ControlVariable': mess[2],
                'ErrorSum': mess[3],
                'MPCHorizonLength': int(mess[4]),
                'MPCQ': mess[5],
                'MPCR': mess[6],
                'ControllerType': mess[-1]
            }
            # Resetting average time of communication
            if data['ControllerType'] != previous_controller_type:
                previous_controller_type = data['ControllerType']
                time_sum = 0
                msg_count = 0
            try:
                time1 = time.perf_counter_ns()
                response = session.post(url, json=data, timeout=0.09)
                time2 = (time.perf_counter_ns() - time1)/1000000
                time_sum += time2
                msg_count += 1
                average = time_sum / msg_count
                if response.status_code == 200:
                    result = response.json()
                    output = result['result']
                    operation_time = result['operation_time']
                    cpa_val = result['cpa_val']
                    print(f"Data received: from broker: {mess};from server: {float(output):.4f};"
                          f"time elapsed: {time2} ms; average time: {average:.4f};"
                          f"server operation time: {operation_time} ms")
                    publish(client, cloud_topic, str(random.randint(100000, 999999))
                            + "{0:.6f}".format(float(output))[:6])
                    cpa_val.extend([data['ControlVariable'], time2, operation_time])
                    writer.writerow(cpa_val)
                else:
                    print('Error:', response.status_code, response.json()
                          + f"Data received: from broker: {mess}; time elapsed: {time2} ms")
            except MQTTException:
                print("Error while sending data to Broker! (trying again)")
            except requests.RequestException:
                print("Error while sending data to Cloud - server not responding! (trying again)")

    client.subscribe(topic)
    client.on_message = on_message


def publish(client: mqtt_client, topic: str, message: str):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"Message published successfully to <{broker}>, topic: <{topic}>!")
    else:
        print("Failed to publish message")


def run():
    global session
    load_vulnerable_data()
    client = None
    while session is None:
        try:
            session = requests.Session()
            session.get(url)
        except requests.exceptions.ConnectionError:
            session = None
            print("Server unavailable - trying again in 1 second")
            time.sleep(1)
        else:
            print(f"Succesfully connected to server <{url}>!")
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
