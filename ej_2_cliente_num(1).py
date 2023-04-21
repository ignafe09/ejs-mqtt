from paho.mqtt.client import Client
from time import sleep
import sys
from sympy import isprime
    

def on_connect(client, userdata, rc):
    print("Conectado con código de resultado: " + str(rc)) #rc indica si se ha conectado o no
    client.subscribe('numbers')

#Recibe un mensaje, le suma 1 a su posicion en lista frecuencias, si es entero 
#lo anade a enteros, si no a comaflotante, y devuelve por pantalla si es primo o no

def on_message(client, userdata, msg): 
    print(msg.topic, msg.payload)
    data = msg.payload          
        
    try:
        num = float(data)
        if n // 1 == 0.0: #Es coma flotante
            client.publish('/clients/reales',msg.payload)
            userdata['frecuencia']['reales'] += 1
            client.publish('/clients/frecreales', f'{userdata["frecuencia"]["reales"]}')
        else:
            n= int(msg.payload)
            if isprime(n):
                client.publish('/clients/enteros',f'{n} es primo')
            userdata['frecuencia']['enteros'] += 1
            client.publish('/clients/frecenteros', f'{userdata["frecuencia"]["enteros"]}')
            userdata['suma']['suma'] += n
            client.publish('/clients/suma', f'{userdata["suma"]["suma"]}')
            if n % 2 == 0:
                client.publish('/clients/par', n)
            else:
                client.publish('/clients/impar', n)
    except ValueError:
        pass
    except Exception as e:
        raise e        
                       
def main(hostname):
    userdata = {'suma' : {'suma':0},
                'frecuencia' :{'enteros':0,'reales':0}}
    client = Client(userdata = userdata)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(hostname)
    client.loop_start()
    
    while True:
        sleep(1)


if __name__ == '__main__':
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    hostname = sys.argv[1]
    main(hostname)


