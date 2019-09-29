import base64
import cv2
import zmq
from main import Compressor
import numpy as np


def main():
    context = zmq.Context()
    pub_socket = context.socket(zmq.PUB)
    pub_socket.connect('tcp://localhost:5555')

    camera = cv2.VideoCapture(0)  # init the camera
    compressor = Compressor()
    while True:
        try:
            grabbed, frame = camera.read()  # grab the current frame
            frame = compressor.compress_frame(frame)
            encoded, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)
            pub_socket.send(jpg_as_text)
            frame = pub_socket.recv()
            img = base64.b64decode(frame)
            npimg = np.fromstring(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            cv2.imshow("Stream", frame)
            cv2.waitKey(source)

        except KeyboardInterrupt:
            camera.release()
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
