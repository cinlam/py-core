#import serial

# Paramètres de communication
#port = '/dev/ttyUSB0'  # Port série utilisé pour la communication (ajustez selon votre configuration)
#baudrate = 9600  # Vitesse de transmission en bauds

# Initialisation de la communication série
#ser = serial.Serial(port, baudrate)

# Envoi de données à l'Arduino
#data_to_send = 'Hello Arduino!'
#ser.write(data_to_send.encode())

# Lecture de données depuis l'Arduino
#data_received = ser.readline()
#print('Data received from Arduino:', data_received.decode())

# Fermeture de la communication série
#ser.close()

#import time
#from pylibftdi import Device

# Set the FTDI device index or serial number
#device_id = "FT57MSZM"

# Open the FTDI device using libftdi1
#device = Device(device_id=device_id)

# Set the UART communication parameters
#BAUD_RATE = 9600

# Configure the UART parameters
#device.baudrate = BAUD_RATE
#device.ftdi_fn.ftdi_set_line_property(8, 1, 'N')  # 8 data bits, 1 stop bit, no parity

# Send data over UART
#start_time = time.time()  # Record the start time
#while True:
    #data_to_send = 'A'
    #device.write(data_to_send)
    
    # Exit the loop after 3 seconds
    #if time.time() - start_time >= 3:
        #break

# Wait for the transmission to complete
#time.sleep(3)  # Adjust the delay if necessary


# Read data from UART
#data_received = device.read(len(data_to_send))

# Print the received data
#print("received data :",data_received)

# Close the FTDI device
#device.close()
#while(1):


import time
import struct
from pyftdi.serialext import serial_for_url

# Set the FTDI device URL
device_id = 'ftdi://0x0403:0x6014/1'

# Open the FTDI device
device = serial_for_url(device_id, baudrate=9600)

# Set RTS pin for chip select (CS)
#device.setRTS(True)  # Set RTS pin high to activate chip select

# Send data over SPI
start_time = time.time()  # Record the start time
while True:
    data_to_send = b'\x01\x02\x03'  # Example SPI data
    
    # Transmit SPI data
    device.write(data_to_send)
    
    # Exit the loop after 3 seconds
    if time.time() - start_time >= 1:
        break

# Wait for the transmission to complete
time.sleep(1)  # Adjust the delay if necessary

# Set RTS pin low to deactivate chip select
#device.setRTS(False)

# Read data from UART
data_received = device.read(3)  # Read up to 256 bytes of data

# Decode the received data as an integer
received_value = struct.unpack('!BBB', data_received)

# Print the received value
print("Received value:", received_value)

# Close the FTDI device
device.close()






