import time
from pyftdi import ftdi
from pyftdi.serialext import serial_for_url

# Configuration de la communication série RS-422
#device_id = 'ftdi://ftdi:232h:FT5NX07R/1'
#port = serial_for_url(device_id, baudrate=115200)

# Configuration de la communication série RS-422
device_id = '0403:6001'  # ID du convertisseur FTDI
product = 'FT232H Single HS USB-UART/FIFO IC'  # Produit correspondant au convertisseur FTDI

# Initialisation de l'objet Ftdi
port = ftdi.Ftdi()
port.open(device_id, product)  # Ouverture du port série

# Fonction d'envoi de données
def send_data(data):
    port.write(data)  # Envoie les données via le port série
    port.flush()

# Fonction de réception de données
def receive_data():
    data = port.read(100)  # Lire jusqu'à 100 octets de données
    return data

# Ouvrir le port série
port.open()

# Exemple d'utilisation
send_data(b"Hello, Arduino!")  # Envoie les données à l'Arduino
time.sleep(1)  # Attendre 1 seconde
received_data = receive_data()  # Réception des données depuis l'Arduino
print("Données reçues:", received_data.decode())

# Fermeture du port série
port.close()
