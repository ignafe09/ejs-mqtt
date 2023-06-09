import time
import random
import statistics
from paho.mqtt.client import Client
import sys
from time import sleep

#Esto es un ejemplo de cadena de clientes, pero se pueden hacer mas y de otras formas.
values = []

# Función para determinar si un número es primo
def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Función para calcular el valor medio de una lista de valores
def calculate_mean(values):
    if len(values) == 0:
        return 0
    return sum(values) / len(values)

def on_connect(client, rc):
    print("Conectado con código de resultado: " + str(rc))
    client.subscribe('numbers')
    
# Función que se ejecutará cuando se reciba un mensaje en el topic "numbers"
# Lee el numero, si es primo, se pone a escuchar humedad 5 seg.
def on_message_numbers(client, userdata, message):
    number = int(message.payload)
    print(f"Número recibido: {number}")
    if es_primo(number):
        print("Número primo, leyendo humedad durante 5 segundos...")
        values.clear()
        client.subscribe("humidity")
        time.sleep(5) # Esperamos 5 segundos
        client.unsubscribe("humidity")

# Función que se ejecutará cuando se reciba un mensaje en el topic "humidity"
# Mientras escucha humedad, va leyendo mensajes y los añade a una lista,
#cuando llega a recibir 5 mensajes, calcula media y devuelve por pantalla,
#y vacia la lista. Si la media supera cierto valor, se pone un temporizador.

def on_message_humidity(client, userdata, message):
    humidity = float(message.payload)
    print(f"Received humidity: {humidity}")
    values.append(humidity)
    if len(values) >= 5:
        mean = calculate_mean(values)
        print(f"Media humedad: {mean}")
    if mean > 20:
        print('Humdedad umbral superada, poniendo temporizador...')
        client.publish('temporizador', 'humedad_umbral;5;superada')
        



def main(hostname):
    
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message_numbers
    client.message_callback_add("humidity", on_message_humidity)
    client.connect(hostname)
    client.loop_start()
    
    while True:
        sleep(1)

if __name__ == '__main__':
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)


