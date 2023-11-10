for x in range(10):
        print("Testing Ethernet Driver call")
## @file
# @brief Example code for TCP server using sockets.
#
# This code demonstrates how to create a TCP server using sockets in Python.
# It creates a socket object, binds it to a specified interface and port,
# and listens for incoming connections. When a client connects, it receives
# data from the client, processes it, and sends a response back.
#
# @note Make sure to replace the 'interface' and 'port' variables with appropriate values.

import socket

## @brief Create a socket object.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## @brief Set the interface and port to bind the socket.
interface = "eth0"  # Replace with the actual interface name
port = 1234  # Replace with the desired port number

## @brief Bind the socket to the interface and port.
sock.bind((interface, port))

## @brief Listen for incoming connections.
sock.listen(1)

while True:
    ## @brief Accept a connection.
    connection, client_address = sock.accept()
    try:
        print("Connection from:", client_address)

        ## @brief Receive data from the client.
        data = connection.recv(1024)
        if data:
            ## @brief Process the received data.
            print("Received data:", data.decode())

            ## @brief Send a response back to the client.
            response = "Hello, client!"
            connection.sendall(response.encode())
    finally:
        ## @brief Close the connection.
        connection.close()
