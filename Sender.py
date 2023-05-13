import socket

FIRST_ID = 3147
SECOND_ID = 267
HOST = 'localhost'
PORT = 12345
# xor operation between the id's to send an authentication between the sender and the receiver
XOR_OPERATION = str(FIRST_ID ^ SECOND_ID)


def splitting_data(file_name) -> tuple:
    with open(file_name, "rb") as file:
        file_data = file.read()
    # Split the file into two parts (first half and second half)
    file_size = len(file_data)
    half_size = file_size // 2
    first_half = file_data[:half_size]
    second_half = file_data[half_size:]
    return first_half, second_half


def send_file():
    file_name = 'testing_file.txt'
    first_half, second_half = splitting_data(file_name)

    # create TCP connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f"Connected to {HOST} with port {PORT}")
    while True:
        # Send the first half of the file with Reno algorithm and after that closing the socket
        print("Setting the socket to reno CC algorithm")
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'reno')
        # send first part of file
        print("Sending the first part of the file")
        s.sendall(first_half)
        print("finish to send the first part of the file")
        print("-----------------------------------------------------------------------------------")
        # receive authentication response
        print("Waiting for authentication message...")
        auth_response = s.recv(1024).decode()
        if auth_response == XOR_OPERATION:
            print("Authentication Successful")
        else:
            print("Authentication Failed")
            return
        print("-----------------------------------------------------------------------------------")
        # Send the second half of the file with Cubic algorithm and after that closing the socket
        print("Setting the socket to cubic CC algorithm")
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')
        # send second part of file
        print("Sending the second part of the file")
        s.sendall(second_half)
        print("finish to send the second part of the file")
        print("-----------------------------------------------------------------------------------")
        # prompt user to send file again
        receiver_msg = s.recv(7).decode()
        if receiver_msg == "waiting":
            send_again = input("Do you want to send file again? (y/n): ")
            if send_again.lower() == "y":
                s.sendall("y".encode())
                # send_file()
            else:
                s.sendall("n".encode())
                s.close()
                break


send_file()
