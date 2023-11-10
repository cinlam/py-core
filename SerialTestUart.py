from Serial import CommunicationMachine, calculate_crc

def main2():
    """
    Main function for testing communication over UART.
    """
    # Create an instance of the CommunicationMachineclass
    communication_machine = CommunicationMachine()
    data_to_send = b'\x03\x58\x56'  # Example data
    communication_machine.send_uart_packet(data_to_send)

    received_uart_packet = []  # List to store the received packet
    received_packet = communication_machine.read_uart_packet(received_uart_packet)
    
    # Extract the received data and CRC 
    uart_data = bytes(received_packet[1:4]) 

    print("")
    received_crc = int.from_bytes(received_packet[4:6], byteorder='big')  # Extract bytes from index 5 to index 6 (inclusive) and convert to integer
    print("received_crc:",hex(received_crc))
    print("")
        
    # Calculate CRC-16 checksum for the received data
    calculated_crc = calculate_crc(uart_data)
    print("calculated_crc:",hex(calculated_crc))
    print("")
        
    # Compare the received CRC with the calculated CRC
    if received_crc == calculated_crc:
        print("CRC-16 verification successful. No errors detected.")
        print("")
        # Display the received data in hexadecimal
        hex_data = [hex(byte) for byte in uart_data]
        # Display the received data
        print("Received UART data:", hex_data)
        print("")
    else:
        print("CRC-16 verification failed. Errors detected in the received data.")
        print("Failed to receive UART data.")

if __name__ == "__main__":
    main2()
