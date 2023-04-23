import socket
import os

# Define the IP address and Port number of the Receiver
receiver_ip = '127.0.0.1'
receiver_port = 5005

# Define the path to the file to be sent
file_path = 'vector.txt'

# Open the file and read its contents
with open(file_path, 'rb') as f:
    file_data = f.read()

# Create a TCP socket and connect to the Receiver
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((receiver_ip, receiver_port))

# Send the first half of the file
file_size = os.path.getsize(file_path)
first_half_size = file_size // 2
s.sendall(file_data[:first_half_size])

# Wait for authentication from the Receiver
response = s.recv(1024)

# Check for authentication
if response == b'AUTHENTICATED':
    print('Authentication successful')
else:
    print('Authentication failed')

# Change the CC algorithm
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION_ALGORITHM, b'e2e')

# Send the second half of the file
s.sendall(file_data[first_half_size:])

# Ask the user if they want to send the file again
while True:
    answer = input('Do you want to send the file again? (Y/N) ')
    if answer.upper() == 'Y':
        # Notify the Receiver
        s.sendall(b'SEND AGAIN')

        # Change the CC algorithm back to the default
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION_ALGORITHM, b'reno')

        # Send the first half of the file again
        s.sendall(file_data[:first_half_size])

        # Wait for authentication from the Receiver
        response = s.recv(1024)

        # Check for authentication
        if response == b'AUTHENTICATED':
            print('Authentication successful')
        else:
            print('Authentication failed')

        # Change the CC algorithm
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION_ALGORITHM, b'e2e')

        # Send the second half of the file again
        s.sendall(file_data[first_half_size:])
    elif answer.upper() == 'N':
        # Say bye to the Receiver
        s.sendall(b'EXIT')

        # Close the TCP connection
        s.close()
        break
    else:
        print('Invalid answer, please try again.')
