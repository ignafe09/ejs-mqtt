from paho.mqtt.client import Client
from time import sleep
import sys

#calcula maximo, minimo, medias, devuelve por pantalla y vacia las listas
def calculate_statistics(userdata):
    t1= userdata["t1_temperatures"]
    t2= userdata["t2_temperatures"]
    t1_max = max(t1)
    t1_min = min(t2)
    t1_media = sum(t1) / len(t1)
    t2_max = max(t2)
    t2_min = min(t2)
    t2_media = sum(t2) / len(t2)
    print(f'SENSOR 1 - Max: {t1_max}, Min: {t1_min}, Media: {t1_media}')
    print(f'SENSOR 2 - Max: {t2_max}, Min: {t2_min}, Media: {t2_media}')

def on_connect(client, rc):
    print("Conectado con código de resultado: " + str(rc))
    client.subscribe('temperature/t1')
    client.subscribe('temperature/t2')

#recibe mensaje, y dependiendo de donde venga, lo anade a una lista en userdata u otra
def on_message(client, userdata, msg):
    try:
        print(msg.topic, msg.payload)
        data = msg.payload
        topic=msg.topic
        if topic == 'temperature/t1':
            userdata["t1_temperatures"].append(float(data))
        elif topic == 'temperature/t2':
            userdata["t2_temperatures"].append(float(data))
    except ValueError:
        pass
    except Exception as e:
        raise e

# función principal, cada 5 segundos va calculando las estadisticas y las devuelve por pantalla
def main(hostname):
    userdata = {'t1_temperatures':[],'t2_temperatures':[]}
    client = Client(userdata=userdata)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(hostname)
    client.loop_start()

    while True:
        sleep(5) #Esperamos 5 segundos
        calculate_statistics(userdata)


if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    hostname=sys.argv[1]
    main(hostname)
