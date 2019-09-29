import pickle
import socket
import struct

import cv2


def get_data(conn):
    data_size = 4096
    data = b''  ### CHANGED
    payload_size = struct.calcsize("L")  ### CHANGED

    # Retrieve message size
    while len(data) < payload_size:
        data += conn.recv(data_size)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]  ### CHANGED

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += conn.recv(data_size)

    frame_data = data[:msg_size]
    data = data[msg_size:]
    return data

    # # Extract frame
    # frame = pickle.loads(frame_data)
    # # Display
    # # cv2.imshow('frame', frame)
    # # cv2.waitKey(1)
    # return frame


def manage_clients(clients):
    if len(clients) != 2:
        return
    else:
        frame1 = get_data(clients[0])
        frame2 = get_data(clients[1])
        clients[0].send(frame1)
        clients[1].send(frame2)
        print('frames sent')
        clients[0].close()
        clients[1].close()

def main():
    HOST = ''
    PORT = 8089

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST, PORT))
    print('Socket bind complete')
    s.listen(2)
    print('Socket now listening')

    clients = []
    try:
        while True:
            print(clients)
            if len(clients)<2:
                conn, addr = s.accept()
                clients.append(conn)
            else:
                manage_clients(clients)
                clients = []
    except KeyboardInterrupt:
        s.close()
main()