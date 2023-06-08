import random

from paho.mqtt import client as mqtt_client

broker = '192.168.1.100'
port = 1883
topic = "siemens"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'simatic'
password = 'SecureConnection'
# store password and username in secure file


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
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
        print("Message content: " + str(msg.payload.decode()))
        publish(client, "other_topic", msg.payload.decode())
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