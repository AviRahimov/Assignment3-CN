import socket
import time

# Define the IP address and port to listen on
IP = '0.0.0.0'  # listen on all available network interfaces
PORT = 12345  # choose a port number to listen on

# Create a TCP socket and bind it to the IP address and port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP, PORT))

    # Listen for incoming connections
    s.listen()

    print(f"Receiver listening on {IP}:{PORT}")

    while True:
        # Accept a new connection
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            # Set the congestion control algorithm to Reno for the first half
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'reno')

            # Receive the first half of the file
            start_time = time.monotonic()
            data = conn.recv(8192)
            while data:
                data = conn.recv(8192)
            end_time = time.monotonic()

            # Calculate the time taken to receive the first half of the file
            first_half_time = end_time - start_time

            # Set the congestion control algorithm to Cubic for the second half
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')

            # Receive the second half of the file
            start_time = time.monotonic()
            data = conn.recv(8192)
            while data:
                data = conn.recv(8192)
            end_time = time.monotonic()

            # Calculate the time taken to receive the second half of the file
            second_half_time = end_time - start_time

            # Calculate the total time taken to receive the file
            total_time = first_half_time + second_half_time

            # Print the time taken to receive the file
            print(f"File received in {total_time:.2f} seconds")
