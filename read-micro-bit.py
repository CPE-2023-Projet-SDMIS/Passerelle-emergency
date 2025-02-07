import serial
import json
from time import time
import requests

# Port série utilisé
port = '/dev/ttyACM0'

API_URL = "http://45.158.77.26:8080"

# Paramètres de la communication série
baudrate = 115200 

try:
    # Ouvrir le port série
    ser = serial.Serial(port, baudrate)

    while True:

        # Lire une ligne de données depuis le port série
        line = ser.readline().decode('utf-8').strip()

        reveived = line.split(" ")
        senderID = reveived[0]
        receiverID = reveived[1]
        message = reveived[2:]


        for i in range(0, len(message), 2):
            if int(message[i]) != 0:
                json_data =  '{"sensorID":' + message[i] + ',"intensity":' + message[i+1] + '}'
                print(json_data)
                json_data = json.loads(json_data)
                #print(json_data['sensorID'])
                requests.post(API_URL + "/api/passerelle/addSensorEvent", json=json_data)

except serial.SerialException:
    print(f"Le port série {port} n'a pas pu être ouvert. Assurez-vous que le périphérique est correctement connecté.")
except KeyboardInterrupt:
    # Gérer l'interruption (Ctrl+C) pour fermer proprement le port série
    ser.close()
    print("Fermeture du port série.")
