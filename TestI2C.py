from Serial import CommunicationMachine, calculate_crc

def main1():
    """
    Main function for testing communication over SPI.
    """
    # Create an instance of the CommunicationMachine class
    communication_machine = CommunicationMachine()
    data_to_send = [0x99, 0x88, 0x77]  # Example data
    #register = 0x10
    #communication_machine.send_I2C_packet(register,data_to_send)
    communication_machine.send_I2C_packet(data_to_send)

    received_spi_data = []  # List to store the received data
    received_data = communication_machine.read_spi_packet(received_spi_data)
    print("I²C received data",received_data)
    
if __name__ == "__main__":
    main1()

