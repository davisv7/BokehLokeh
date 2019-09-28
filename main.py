import PySimpleGUI as gui
import cv2
import sys
from PIL import Image
import io


class Compressor:
    def __init__(self):
        faceCascPath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + faceCascPath)

        # profileCascPath = "haarcascade_profileface.xml"
        # profileCascade = cv2.CascadeClassifier(cv2.data.haarcascades + profileCascPath)
        #
        # bodyCascPath = "haarcascade_fullbody.xml"
        # bodyCascade = cv2.CascadeClassifier(cv2.data.haarcascades + bodyCascPath)

    def compress_frame(self, frame):
        shape = frame.shape
        width, height, _ = shape
        pixelSize = 64
        # Resize input to "pixelated" size
        temp = cv2.resize(frame, (pixelSize, pixelSize), interpolation=cv2.INTER_LINEAR)
        # Initialize output image
        pixelatedFrame = cv2.resize(temp, (height, width), interpolation=cv2.INTER_NEAREST)
        # print(pixelatedFrame.shape, frame.shape)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            # minSize=(30, 30),
        )
        # profiles = profileCascade.detectMultiScale(
        #     gray,
        #     scaleFactor=1.2,
        #     minNeighbors=5,
        #     minSize=(10, 10),
        # )
        # bodies = bodyCascade.detectMultiScale(
        #     gray,
        #     scaleFactor=1.2,
        #     minNeighbors=5,
        #     minSize=(10, 10),
        # )

        # features = [*profiles, *faces]
        # features = [*bodies, *faces]
        features = faces
        # features = bodies
        # features = profiles
        for (x, y, w, h) in features:
            proi = pixelatedFrame[y:y + h, x:x + w]
            froi = frame[y:y + h, x:x + w]
            cv2.rectangle(img=pixelatedFrame, pt1=(x, y), pt2=(x + w - 1, y + h - 1), color=(0, 0, 0), thickness=-1)

            # center = (2*x + w - 1)//2,(2*y + h - 1)//2
            # cv2.circle(img=pixelatedFrame, center=center, radius = (y + h - 1)//4, color=(0, 0, 0), thickness=-1)
            dst = cv2.add(froi, proi)
            pixelatedFrame[y:y + h, x:x + w] = dst
        return pixelatedFrame


# helper code: https://www.reddit.com/r/Python/comments/9mkukj/webcam_playback_inside_of_a_gui_using_opencv/

def main():
    layout = [[gui.Text('OpenCV', size=(40, 1), justification='center', font='Helvetica 20')],
              [gui.Image(filename='', key='image')],
              [gui.ReadButton('Switch', size=(10, 1), pad=((200, 0), 3), font='Helvetica 14')],
              [gui.ReadButton('Exit', size=(10, 1), pad=((200, 0), 3), font='Helvetica 14')]]

    window = gui.Window('Demo', location=(800, 400))
    window.Layout(layout).Finalize()
    state = True
    # window.Layout(layout)
    # window.Read()
    video_capture = cv2.VideoCapture(0)

    compressor = Compressor()

    # log.basicConfig(filename='webcam.log', level=log.INFO)

    while True:
        button, values = window._ReadNonBlocking()

        if button is 'Exit' or values is None:
            sys.exit(0)
        elif button is 'Switch':
            state = (state + 1) % 2

        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if state:
            usedFrame = compressor.compress_frame(frame)
        else:
            usedFrame = frame

        imgbytes = cv2.imencode('.png', usedFrame)[1].tobytes()  # ditto
        print('{} kb/s'.format(len(imgbytes) // 1000))
        window.FindElement('image').Update(data=imgbytes)

if __name__ == '__main__':

    main()
