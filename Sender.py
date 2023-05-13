import socket
import time


def send_file():
    file_name = 'testing_file.txt'
    with open(file_name, "rb") as file:
        file_data = file.read()

    # create TCP connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    first_id = 3147
    second_id = 267
    # xor operation between the id's to send an authentication between the sender and the receiver
    xor_operation = str(first_id ^ second_id)
    host = "127.0.0.1"
    port = 12345
    s.connect((host, port))

    # Send the first half of the file with Reno algorithm and after that closing the socket
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'reno')
    # send first part of file
    s.sendall(file_data[:len(file_data) // 2])

    # receive authentication response
    auth_response = s.recv(1024).decode()
    if auth_response == xor_operation:
        print("Authentication Successful")
    else:
        print("Authentication Failed")
        return

    # Send the second half of the file with Cubic algorithm and after that closing the socket
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')
    # send second part of file
    s.sendall(file_data[len(file_data) // 2:])

    # prompt user to send file again
    send_again = input("Send file again? (y/n): ")
    if send_again.lower() == "y":
        s.sendall("Send Again".encode())
        # change back the congestion control algorithm
        # ...
        send_file()
    else:
        s.sendall("Exit".encode())
        s.close()


send_file()
