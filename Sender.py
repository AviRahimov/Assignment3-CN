import socket
import time

# Define the IP address and port of the receiver
IP = '127.0.0.1'  # replace with the receiver's IP address
PORT = 12345  # replace with the receiver's port number

# Define the filename and read the file
FILENAME = 'testing_file.txt'  # replace with the name of the file to be sent
with open(FILENAME, 'rb') as file:
    file_data = file.read()

# Split the file into two parts (first half and second half)
file_size = len(file_data)
half_size = file_size // 2
first_half = file_data[:half_size]
second_half = file_data[half_size:]
# Create a TCP socket and connect to the receiver
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Enable TCP Fast Open on the socket
    s.setsockopt(socket.SOL_TCP, socket.TCP_FASTOPEN, 100)

    # Connect to the receiver
    s.connect((IP, PORT))

    # Send the first half of the file with Reno algorithm
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'reno')
    s.send(first_half)
    # Send the second half of the file with Cubic algorithm
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')
    s.send(second_half)
