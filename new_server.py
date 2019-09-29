import base64
import cv2
import zmq
import numpy as np
from main import Compressor


def main():
    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)
    sub_socket.bind('tcp://*:5555')
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    camera = cv2.VideoCapture(0)  # init the camera
    compressor = Compressor()
    while True:
        try:
            frame = sub_socket.recv()
            img = base64.b64decode(frame)
            npimg = np.fromstring(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            cv2.imshow("Stream", frame)
            cv2.waitKey(source)
            grabbed, frame = camera.read()  # grab the current frame
            frame = compressor.compress_frame(frame)
            encoded, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)
            sub_socket.send(jpg_as_text)


        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
