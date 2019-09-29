import cv2
import numpy as np
import socket
import sys
import pickle
import struct
from main import Compressor
from random import randint


def main():
    data_size = 4096
    cap = cv2.VideoCapture(0)

    payload_size = struct.calcsize("L")  ### CHANGED
    try:
        while True:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.connect(('localhost', 8089))
            compressor = Compressor()
            ret, frame = cap.read()
            frame = compressor.compress_frame(frame)
            # Serialize frame
            data = pickle.dumps(frame)
            # data = pickle.dumps([randint(0, 1000) for i in range(1000)])
            # Send message length first
            message_size = struct.pack("L", len(data))  ### CHANGED

            # Then data
            clientsocket.sendall(message_size + data)
            msg_size = struct.unpack("L", message_size)[0]
            data = b''  ### CHANGED
            while len(data) < payload_size:
                data += clientsocket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            # Extract frame
            if frame_data:
                frame = pickle.loads(frame_data)
                # Display
                cv2.imshow('frame', frame)
                cv2.waitKey(1)
                # return frame
                # print("received frame!")
            else:
                clientsocket.close()
    except KeyboardInterrupt:
        clientsocket.close()


main()
