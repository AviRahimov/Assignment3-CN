import socket
import time

def receive_file():
    # create TCP connection and bind it to the IP address and port
    s = socket.socket()
    # Define the IP address and port to listen on
    # listen on all available network interfaces
    host = 'localhost'
    # port number to listen on
    port = 12345
    first_id = 3147
    second_id = 267
    xor_operation = str(first_id ^ second_id).encode()
    buffer_size = 4096
    times_list_first_part = []
    times_list_second_part = []
    s.bind((host, port))
    # Listen for incoming connections
    s.listen(1)
    # Accept a new connection
    conn, addr = s.accept()
    # Set the congestion control algorithm to Reno for the first half
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'reno')
    # receive first part of file
    start_time = time.time()
    data = b""
    print("Receiving the first half of the file from the sender")
    while len(data) < buffer_size*buffer_size:
        packet = conn.recv(buffer_size)
        if not packet:
            break
        data += packet
    print("Done received the first half")
    end_time = time.time()

    # measure time to receive first part of file
    first_part_time = end_time - start_time
    times_list_first_part.append(first_part_time)

    print("Sending authentication")
    conn.sendall(xor_operation)

    # Set the congestion control algorithm to Cubic for the second half
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')

    # receive second part of file
    start_time = time.time()
    data = b""
    print("Receiving the second half of the file from the sender")
    while len(data) < buffer_size*buffer_size:
        packet = conn.recv(buffer_size)
        if not packet:
            break
        data += packet
    print("Done received the second half")
    end_time = time.time()

    # measure time to receive second part of file
    second_part_time = end_time - start_time
    times_list_second_part.append(second_part_time)

    print("Waiting for the sender to send more files or to close the connection...")
    # check if sender wants to send file again or exit
    msg = conn.recv(buffer_size).decode()
    if msg == "Send Again":
        print("Receiving more files!")
        print("-----------------------------------------------------------------------------------")
        receive_file()
    elif msg == "Exit":
        print("-----------------------------------------------------------------------------------")
        print("Calculating times: ")
        # calculate average time
        avg_first_part_time = first_part_time
        avg_second_part_time = second_part_time
        total_time = avg_first_part_time + avg_second_part_time
        print("Average time to receive first part of file: ", avg_first_part_time)
        print("Average time to receive second part of file: ", avg_second_part_time)
        print("Total time taken to receive file: ", total_time)
        # close TCP connection
        conn.sendall("Goodbye".encode())
        conn.close()
    else:
        # if message is not recognized, close TCP connection
        conn.sendall("Invalid Message".encode())
        conn.close()

        receive_file()
