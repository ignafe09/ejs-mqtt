from paho.mqtt.client import Client
from time import sleep
import sys


def on_connect(client, rc):
    print("Conectado con código de resultado: " + str(rc))
    client.subscribe('temporizador')

#se recibe un mensaje con un tiempo de espera, se hace un sleep del tiempo que se indica,
# y se publica cuando ha terminado
def on_message(client, userdata, msg):
    dato = msg.payload
    topic, espera, mensaje = dato.split(';')
    t_espera = int(espera)
    sleep(t_espera)
    client.publish(topic,  mensaje)

# función principal
def main(hostname):
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(hostname)
    client.loop_start()

    while True:
        sleep(1)


if __name__ == '__main__':
    if len(sys.argv)>1:
        print(f"Usage: {sys.argv[0]}")
    hostname = sys.argv[1]
    main(hostname)

