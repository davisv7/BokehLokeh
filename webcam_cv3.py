import cv2
from time import sleep
import numpy as np

faceCascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + faceCascPath)

profileCascPath = "haarcascade_profileface.xml"
profileCascade = cv2.CascadeClassifier(cv2.data.haarcascades + profileCascPath)

bodyCascPath = "haarcascade_fullbody.xml"
bodyCascade = cv2.CascadeClassifier(cv2.data.haarcascades+bodyCascPath)

# log.basicConfig(filename='webcam.log', level=log.INFO)

video_capture = cv2.VideoCapture("test-before.mp4")
anterior = 0

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    shape = frame.shape
    width, height, _ = shape
    ratio = width / height
    # print(ratio)
    pixelWidth = 128
    # Resize input to "pixelated" size
    temp = cv2.resize(frame, (pixelWidth, pixelWidth), interpolation=cv2.INTER_LINEAR)
    # Initialize output image
    pixelatedFrame = cv2.resize(temp, (height, width), interpolation=cv2.INTER_NEAREST)
    # print(pixelatedFrame.shape, frame.shape)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
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
    # Draw a rectangle around the faces
    for (x, y, w, h) in features:
        proi = pixelatedFrame[y:y + h, x:x + w]
        froi = frame[y:y + h, x:x + w]
        cv2.rectangle(img=pixelatedFrame, pt1=(x, y), pt2=(x + w - 1, y + h - 1), color=(0, 0, 0), thickness=-1)
        dst = cv2.add(froi, proi)
        pixelatedFrame[y:y + h, x:x + w] = dst

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', pixelatedFrame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
