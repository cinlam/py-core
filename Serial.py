# Import required libraries
import crcmod.predefined
import smbus
import can
import array
import time
from time import sleep
from pylibftdi import Device
from pyftdi.serialext import serial_for_url
import pyftdi.spi as spi
import pyftdi.ftdi as ftdi
import pyftdi.usbtools as usbtools
from pyftdi.i2c import I2cController, I2cNackError


# Pin mapping SPIcl
spi_clk = 2  # Clock (SK)
spi_do = 3  # Data out (DO)
spi_di = 4  # Data in (DI)
spi_cs = 0  # Chip select (CS)

def calculate_crc(data):
    """
    Calculate CRC-16 value for the given data.
    Args:
        data (list): List of bytes.
    Returns:
        int: CRC-16 value.
    """
    crc_value = 0xFFFF  # Initial CRC-16 value

    for byte in data:
        crc_value ^= byte

        for _ in range(8):
            if crc_value & 0x0001 != 0:
                crc_value >>= 1
                crc_value ^= 0xA001  # CRC-16 polynomial (0xA001)
            else:
                crc_value >>= 1

    return crc_value

def packet_formatting(data):
    """
    Format the data packet by appending CRC and start marker.
    Args:
        data (list): List of bytes.
    Returns:
        list: Formatted data packet.
    """
    # Calculate CRC from data
    crc_calc = calculate_crc(data)

    # Print the CRC value
    print("CRC-16: {:04X}".format(crc_calc))

    # Convert CRC value to bytes
    crc_bytes = crc_calc.to_bytes(2, byteorder='big')  # Assuming CRC-16 is 2 bytes long

    # Append CRC bytes to data
    start_marker = 0xAA
    packet = [start_marker] + list(data) + list(crc_bytes)

    print("Sending packet:", packet)

    return packet

class CommunicationMachine(object):
    """
    State machine for communication.
    """


    #def send_I2C_packet(self, register, data):
    def send_I2C_packet(self,data):
        """
        Send data packet over I2C.
        Args:
            register (int): Register address.
            data (list): List of bytes.
        """
        packet = packet_formatting(data)
        
        # Arduino slave address (address depends on hardware configuration)
        arduino_address = 0x04

        # Configure the I2C controller
        ctrl = I2cController()

        # Open the I2C connection with the FTDI converter
        url = 'ftdi://ftdi:232h:FT57MSZM/1'  # FTDI converter URL
        ctrl.configure(url)

        # Get the I2C interface
        i2c = ctrl.get_port(arduino_address)
        
        # Send data to Arduino with a specific register
        #i2c.write_to(register, packet)
        # Send data to Arduino with only data
        i2c.write(packet)

    def read_I2C_packet(self, received_packet):
        """
        Read data packet over I2C.
        Args:
            received_packet (list): List to store received packet.
        Returns:
            list: Received data packet.
        """
        # Arduino slave address (address depends on hardware configuration)
        arduino_address = 0x04

        # Specific register to use
        #register = 0x10

        # Configure the I2C controller
        ctrl = I2cController()

        # Open the I2C connection with the FTDI converter
        url = 'ftdi://ftdi:232h:FT57MSZM/1'  # FTDI converter URL
        ctrl.configure(url)

        # Get the I2C interface
        i2c = ctrl.get_port(arduino_address)
        # Receive data from Arduino from a specific register
        #received_packet = i2c.read(1)[0]
        # Read data from Arduino
        received_packet = i2c.read(1)  # Read 3 byte
        # print I²C received data
        print("Data received from Arduino:", received_packet)
        
        return received_packet
    
    def send_spi_packet(self, data):
        """
        Send data packet over SPI.
        Args:
            data (list): List of bytes.
        """
        packet = packet_formatting(data)

        # Configure SPI pins and settings
        spi_device = spi.SpiController()
        spi_device.configure('ftdi://ftdi:232h:FT57MSZM/1', cs_count=1)  # 'ftdi://ftdi:232h/1' is used to indicate the USB port

        # Get the SpiPort object for the specified SPI channel
        spi_port = spi_device.get_port(cs=spi_cs, freq=6E6, mode=3)  # mode=0 for mode 0 (CPOL=0, CPHA=0)
        spi_port.set_frequency(6E6)  # Set SPI frequency
        spi_port.set_mode(0)  # Set SPI mode to 0 (CPOL=0,CPHA=0)

        # Send data
        start_time = time.time()  # Record the start time
        while True:
            # Transmit SPI data
            spi_port.write(packet)  # Send data to Arduino via SPI



            # Exit the loop after 3 seconds
            if time.time() - start_time >= 2:
                break

        spi_device.terminate()  # Release SPI resources

    def read_spi_packet(self, received_data):
        """
        Read data packet over SPI.
        Args:
            received_data (list): List to store received data.
        Returns:
            list: Received data packet.
        """
        spi_device = spi.SpiController()
        spi_device.configure('ftdi://ftdi:232h:FT57MSZM/1', cs_count=1)  # 'ftdi://ftdi:232h/1' is used to indicate the USB port

        spi_port = spi_device.get_port(cs=spi_cs, freq=6E6, mode=3)  # mode=0 for mode 0 (CPOL=0, CPHA=0)
        spi_port.set_frequency(6E6)  # Set SPI frequency
        spi_port.set_mode(0)  # Set SPI mode to 0 (CPOL=0, CPHA=0)

        start_byte = 0xBB  # Start byte value
        end_byte = 0xAA  # End byte value
        start_byte_received = False

        while True:
            rx_byte = spi_port.read(1)  # Read a byte of data from Arduino via SPI

            if not start_byte_received:
                if rx_byte[0] == start_byte:
                    start_byte_received = True
                    received_data.append(rx_byte[0])
            else:
                if rx_byte[0] != 0x00 and rx_byte[0] != 0xFF:  # Filter unwanted bytes
                    received_data.append(rx_byte[0])

                if rx_byte[0] == end_byte:
                    break

        spi_device.terminate()  # Release SPI resources

        return received_data

    def send_uart_packet(self, data):
        """
        Send data packet over UART.
        Args:
            data (list): List of bytes.
        """
        packet = packet_formatting(data)

        # UART sending logic
        device_id = 'ftdi://ftdi:232h:FTVBYSLK/1'  # Set the FTDI device URL
        device = serial_for_url(device_id, baudrate=9600)  # Open the FTDI device
        device.setRTS(True)  # Set RTS pin high to activate chip select

        start_time = time.time()  # Record the start time
        while True:
            # Transmit UART data
            device.write(packet)

            # Exit the loop after 3 seconds
            if time.time() - start_time >= 2:
                break

        device.close()  # Close the UART device

    def read_uart_packet(self, received_packet):
        """
        Read data packet over UART.
        Args:
            received_packet (list): List to store received packet.
        Returns:
            list: Received data packet.
        """
        device_id = 'ftdi://ftdi:232h:FTVBYSLK/1'  # Set the FTDI device URL
        device = serial_for_url(device_id, baudrate=9600)  # Open the FTDI device

        num_bytes = 5  # Number of bytes to read

        received_packet = []  # Initialize an empty list
        start_byte = b'\xBB'  # Start byte value
        end_byte = b'\xAA'  # End byte value

        while True:
            byte1 = device.read(1)  # Read a single byte from UART

            if byte1 == start_byte:  # Check if start byte is received
                read_data = device.read(num_bytes)  # Read the next 5 bytes
                byte6 = device.read(1)  # Read the last byte

                if byte6 == end_byte:  # Check if end byte is received
                    received_packet = byte1 + read_data + byte6
                    break

        device.close()  # Close the UART device

        return received_packet
    def send_rs422_packet(self, data):
        """
        Send data packet over RS232.
        Args:
            data (list): List of bytes.
        """
        #FT5NX07R
        device_id = 'ftdi://ftdi:232h:FT5NX07R/1'
        packet = packet_formatting(data)
        print("")

    def read_rs422_packet(self, received_packet):
        """
        Read data packet over RS232.
        Args:
            received_packet (list): List to store received packet.
        Returns:
            list: Received data packet.
        """
        print("Implement RS232")
        return received_packet
    def send_rs232_packet(self, data):
        """
        Send data packet over RS232.
        Args:
            data (list): List of bytes.
        """
        packet = packet_formatting(data)
        print("")

    def read_rs232_packet(self, received_packet):
        """
        Read data packet over RS232.
        Args:
            received_packet (list): List to store received packet.
        Returns:
            list: Received data packet.
        """
        print("Implement RS232")
        return received_packet

    def send_can_packet(self, data):
        """
        Send data packet over CAN bus.
        Args:
            data (list): List of bytes.
        """
        packet = packet_formatting(data)
        print("")

    def read_can_packet(self, received_packet):
        """
        Read data packet over CAN bus.
        Args:
            received_packet (list): List to store received packet.
        Returns:
            list: Received data packet.
        """
        print("Implement CAN")
        return received_packet

    def send_ethernet_packet(self, data):
        """
        Send data packet over Ethernet.
        Args:
            data (list): List of bytes.
        """
        packet = packet_formatting(data)
        print("")

    def read_ethernet_packet(self, received_packet):
        """
        Read data packet over Ethernet.
        Args:
            received_packet (list): List to store received packet.
        Returns:
            list: Received data packet.
        """
        print("Implement Ethernet")
        return received_packet


# Create an instance of CommunicationStateMachine
communication_machine = CommunicationMachine()

