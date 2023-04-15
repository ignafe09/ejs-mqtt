from paho.mqtt.client import Client
from time import sleep
import sys


def on_connect(client, rc):
    print("Conectado con código de resultado: " + str(rc))
    client.subscribe('temporizador')

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode('utf-8')
    topic, espera, mensaje = payload_str.split(';')
    t_espera = int(espera)
    sleep(t_espera)
    client.publish(topic,  mensaje)

# función principal
def main(hostname):
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set('cliente_temporizador', password=None)
    client.connect(hostname)
    client.loop_start()

    while True:
        sleep(1)


if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]

