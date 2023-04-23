import socket
import time

# Define the IP address and port number
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005

start_time = time.time()
# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP address and port number
sock.bind((SERVER_IP, SERVER_PORT))

# Listen for incoming connections
sock.listen()

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    conn, addr = sock.accept()

    # Print the address of the client that just connected
    print('Connection from:', addr)

    # Receive the first part of the file
    first_part = conn.recv(1024)

    # Send back authentication to the sender
    conn.send(b'AUTHENTICATED')

    # Change the congestion control algorithm
    conn.setsockopt(socket.IPPROTO_TCP, 71, 2)

    # Receive the second part of the file
    second_part = conn.recv(1024)

    # Measure the time it took to receive the entire file
    elapsed_time = time.time() - start_time

    # Print the time it took to receive each part of the file
    print(f'Time to receive first part: {time.time() - start_time:.5f} seconds')
    print(f'Time to receive second part: {time.time() - start_time:.5f} seconds')

    # Check for a SEND AGAIN message from the sender
    send_again_msg = conn.recv(1024)
    if send_again_msg == b'SEND AGAIN':
        # Change the congestion control algorithm back to the default
        conn.setsockopt(socket.IPPROTO_TCP, 71, 1)

        # Receive the first part of the file again
        first_part = conn.recv(1024)

        # Send back authentication to the sender
        conn.send(b'AUTHENTICATED')

        # Change the congestion control algorithm
        conn.setsockopt(socket.IPPROTO_TCP, 71, 2)

        # Receive the second part of the file again
        second_part = conn.recv(1024)

        # Measure the time it took to receive the entire file
        elapsed_time = time.time() - start_time

        # Print the time it took to receive each part of the file
        print(f'Time to receive first part: {time.time() - start_time:.5f} seconds')
        print(f'Time to receive second part: {time.time() - start_time:.5f} seconds')

    # Check for an EXIT message from the sender
    exit_msg = conn.recv(1024).decode()
    if exit_msg == 'EXIT':
        # Calculate the average time it took to receive each part of the file
        avg_first_part_time = (time.time() - start_time) / 2.0
        avg_second_part_time = (time.time() - start_time) / 2.0
        print(f'Average time to receive first part: {avg_first_part_time:.5f} seconds')
        print(f'Average time to receive second part: {avg_second_part_time:.5f} seconds')

        # Close the connection
        conn.close()
        break

    # Close the connection
    conn.close()
