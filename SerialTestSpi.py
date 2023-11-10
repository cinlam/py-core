from Serial import CommunicationMachine, calculate_crc

def main1():
    """
    Main function for testing communication over SPI.
    """
    # Create an instance of the CommunicationMachine class
    communication_machine = CommunicationMachine()
    data_to_send = [0x99, 0x88, 0x77]  # Example data
    communication_machine.send_spi_packet(data_to_send)

    received_spi_data = []  # List to store the received data
    received_data = communication_machine.read_spi_packet(received_spi_data)

    spi_data = bytes(received_data[1:4])

    # Extract the received data and CRC
    print("")
    received_crc = int.from_bytes(received_data[4:6], byteorder='big')  # Extract bytes from index 5 to index 6 (inclusive) and convert to integer
    print("received_crc:", hex(received_crc))
    print("")

    # Calculate CRC-16 checksum for the received data
    calculated_crc = calculate_crc(spi_data)
    print("calculated_crc:", hex(calculated_crc))
    print("")

    # Compare the received CRC with the calculated CRC
    if received_crc == calculated_crc:
        print("CRC-16 verification successful. No errors detected.")
        print("")
        # Display the received data in hexadecimal
        hex_data = [hex(byte) for byte in spi_data]
        # Display the received data
        print("Received SPI data:", hex_data)
        print("")
    else:
        print("CRC-16 verification failed. Errors detected in the received data.")
        print("Failed to receive SPI data.")

if __name__ == "__main__":
    main1()
