from paho.mqtt.client import Client
import sys
from time import sleep

K0 = 25
K1 = 60
listening_humidity = False



#Recibe un mensaje de temperatura1 o temperatura2, si es mayor que un cierto valor K0,
# escucha los mensajes de humidity, si no, deja de escuchar si estaba escuchando.
#una vez recibe de humidity, si es mayor de K1 deja de escuchar y si no no sigue escuchando.
def on_message(mqttc, userdata, msg):
    global listening_humidity
    print(msg.topic, msg.payload)
    dato = float(msg.payload)
    if msg.topic == 'temperature/t1' or msg.topic == 'temperature/t2':
        
        if dato > K0 and not listening_humidity:
            print("Listening to humidity")
            client.subscribe('humidity')
            listening_humidity = True
        elif dato <= K0  and listening_humidity:
            print("Not listening to humidity")
            client.unsubscribe('humidity')
            listening_humidity = False
        
    elif msg.topic == 'humidity'
        if dato > K1 and not listening_humidity:
            print("Listening to humidity")
            client.unsubscribe('humidity')
            listening_humidity = False


def main(hostname):
    client = Client()
    

    client.on_message = on_message

    client.connect(hostname)

    client.subscribe('temperature/t1')
    client.subscribe('temperature/t2')

    client.loop_start()
    
    while True:
        sleep(1)


if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    hostname = sys.argv[1]
    main(hostname)

