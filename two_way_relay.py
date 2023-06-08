import random

from paho.mqtt import client as mqtt_client

broker = '192.168.1.100'
port = 1883
topic = "siemens"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'simatic'
password = 'SecureConnection'