import socket
import time
import os

FIRST_ID = 3147
SECOND_ID = 267
# Define the IP address and port to listen on
HOST = 'localhost'
PORT = 12345
# xor operation between the id's to send an authentication between the sender and the receiver
XOR_OPERATION = str(FIRST_ID ^ SECOND_ID).encode()
BUFFER_SIZE = 4096
times_list_first_part = []
times_list_second_part = []
file_size = os.path.getsize("testing_file.txt")
half_size = file_size // 2


def receive_file():
    # create TCP connection and bind it to the IP address and port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    # Listen for incoming connections
    s.listen()
    # Accept a new connection
    conn, addr = s.accept()
    while True:
        print(f"Connected by {addr}")
        # Set the congestion control algorithm to Reno for the first half
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'reno')
        # receive first part of file
        start_time = time.time()

        print("Receiving the first half of the file from the sender")
        data = b""
        while len(data) < half_size:
            packet = conn.recv(BUFFER_SIZE)
            if not packet:
                break
            data += packet
        print("Done received the first half")
        end_time = time.time()

        # measure time to receive first part of file
        first_part_time = end_time - start_time
        times_list_first_part.append(first_part_time)

        print("Sending authentication")
        conn.sendall(XOR_OPERATION)

        # Set the congestion control algorithm to Cubic for the second half
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')

        # receive second part of file
        start_time = time.time()
        print("Receiving the second half of the file from the sender")
        data = b""
        while len(data) < half_size:
            packet = conn.recv(BUFFER_SIZE)
            if not packet:
                break
            data += packet
        print("Done receiving the second half")
        # conn.sendall(XOR_OPERATION)
        end_time = time.time()
        print("-----------------------------------------------------------------------------------")
        # measure time to receive second part of file
        second_part_time = end_time - start_time
        times_list_second_part.append(second_part_time)

        print("Waiting for the sender to send more files or to close the connection...")
        # check if sender wants to send file again or exit
        conn.sendall("waiting".encode())

        msg = conn.recv(1).decode()
        if msg == "y":
            print("Receiving more files!")
            print("-----------------------------------------------------------------------------------")
            # receive_file()
            continue
        elif msg == "n":
            print("-----------------------------------------------------------------------------------")
            print("Calculating times: ")
            # Calculate the total time taken to receive the file
            avg_time_first_part = sum(times_list_first_part) / len(times_list_first_part)
            avg_time_second_part = sum(times_list_second_part) / len(times_list_second_part)
            # printing the times without average
            print("Sending times for RENO CC algorithm: ")
            for i in range(len(times_list_first_part)):
                print(f"Iteration number: {i + 1}, time: {times_list_first_part[i]}")
            print("-----------------------------------------------------------------------------------")
            print("Sending times for CUBIC CC algorithm: ")
            for i in range(len(times_list_first_part)):
                print(f"Iteration number: {i + 1}, time: {times_list_second_part[i]}")
            print("-----------------------------------------------------------------------------------")
            # Print the time taken to receive the file
            print(f"first half files by RENO algorithm received in average time of {avg_time_first_part} seconds")
            print(f"second half files by CUBIC algorithm received in average time of {avg_time_second_part} seconds")
            break
        else:
            print("Invalid Message occurred")
            # if message is not recognized, close TCP connection
            conn.sendall("Invalid Message".encode())
            conn.close()
            break


receive_file()
