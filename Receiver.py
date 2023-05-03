import socket
import time

# Define the IP address and port to listen on
IP = 'localhost'  # listen on all available network interfaces
PORT = 1234  # choose a port number to listen on
FIRST_ID = 3147
SECOND_ID = 267
xor_operation = str(FIRST_ID ^ SECOND_ID).encode()

buffer_size = 4096
times_list_first_part = []
times_list_second_part = []
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
            start_time = time.time()
            data = conn.recv(buffer_size)
            print("Receiving the first half of the file from the sender")
            while data:
                data = conn.recv(buffer_size)
            end_time = time.time()
            print("Done received the first half")
            # Calculate the time taken to receive the first half of the file
            first_half_time = end_time - start_time
            times_list_first_part.append(first_half_time)

            # connect again to the sender and send an authentication message and after that closing the connection
            conn, addr = s.accept()
            print("Sending authentication")
            conn.sendall(xor_operation)
            conn.close()

            conn, addr = s.accept()
            # Set the congestion control algorithm to Cubic for the second half
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')

            # Receive the second half of the file
            start_time = time.time()
            data = conn.recv(buffer_size)
            print("Receiving the second half of the file from the sender")
            while data:
                data = conn.recv(buffer_size)
            end_time = time.time()
            print("Done received the second half")
            # Calculate the time taken to receive the second half of the file
            second_half_time = end_time - start_time
            times_list_second_part.append(second_half_time)

            conn, addr = s.accept()
            print("Waiting for the sender to send more files or to close the connection...")
            is_done = conn.recv(1024).decode()
            if is_done == "done_sending_all":
                print("-----------------------------------------------------------------------------------")
                print("Connection closed, calculating times: ")
                # Calculate the total time taken to receive the file
                avg_time_first_part = sum(times_list_first_part) / len(times_list_first_part)
                avg_time_second_part = sum(times_list_second_part) / len(times_list_second_part)
                # printing the times without average
                print("Sending times for RENO CC algorithm: ")
                for i in range(len(times_list_first_part)):
                    print(f"Iteration number: {i+1}, time: {times_list_first_part[i]}")
                print("-----------------------------------------------------------------------------------")
                print("Sending times for CUBIC CC algorithm: ")
                for i in range(len(times_list_first_part)):
                    print(f"Iteration number: {i+1}, time: {times_list_second_part[i]}")
                print("-----------------------------------------------------------------------------------")
                # Print the time taken to receive the file
                print(f"first half files by RENO algorithm received in average time of {avg_time_first_part} seconds")
                print(f"second half files by CUBIC algorithm received in average time of {avg_time_second_part} seconds")
                break
            else:
                print("Receiving more files!")
                print("-----------------------------------------------------------------------------------")
                conn.close()
