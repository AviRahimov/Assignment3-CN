import socket
import time
# The ID od the submitters
FIRST_ID = 3147
SECOND_ID = 267
# xor operation between the id's to send an authentication between the sender and the receiver
xor_operation = str(FIRST_ID ^ SECOND_ID)
# Define the IP address and port of the receiver
IP = 'localhost'  # replace with the receiver's IP address
PORT = 1234  # replace with the receiver's port number

# Define the filename and read the file
FILENAME = 'testing_file.txt'  # replace with the name of the file to be sent
with open(FILENAME, 'rb') as file:
    file_data = file.read()

# Split the file into two parts (first half and second half)
file_size = len(file_data)
half_size = file_size // 2
first_half = file_data[:half_size]
second_half = file_data[half_size:]

while True:
    # create a TCP socket and connect to the receiver with specified IP and PORT number
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))

    # Send the first half of the file with Reno algorithm and after that closing the socket
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'reno')
    s.sendall(first_half)
    s.close()

    # connect again and check if the connection is stable with the authentication message
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    authentication = s.recv(1024).decode()

    # if the authentication succeed we create the socket again due to the closing of the receiver server and connect
    if authentication == xor_operation:
        print("authentication succeed")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP, PORT))
        # Send the second half of the file with Cubic algorithm and after that closing the socket
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')
        s.sendall(second_half)
        s.close()
    # if the authentication failed we close the socket and break the loop
    else:
        s.close()
        print("Receiver doesn't send an authentication message")
        break

    send_again = input('Do you want to send the file again? (y/n): ')
    if send_again.lower() != 'y':
        print("Stop sending files")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP, PORT))
        s.sendall("done_sending_all".encode())
        s.close()
        break
    else:
        print("Sending file again!")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP, PORT))
        s.sendall("keep_sending".encode())
        s.close()
