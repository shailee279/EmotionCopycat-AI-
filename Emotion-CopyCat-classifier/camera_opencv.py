import os
import cv2
# import numpy as np
from base_camera import BaseCamera

from emotion_classifiers import classify_emotion

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

        classify_emotion.init_models()
        

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        # init_models()
        classify_emotion.print_stuff()
        

        while True:
            # read current frame
            _, img = camera.read()


            if classify_emotion.face_detector is not None:
                # print('...face_detector is not ready')
                # faces = classify_emotion.get_faces(img)
                img = classify_emotion.mark_faces_in_frame(img)


            # # resize the frame be of height 'height'
            width = 350
            h, w, ch = img.shape
            ratio = width / w
            height = int(h * ratio)
            img = cv2.resize(img, (width, height))
            # print('frame size: ', img.shape)
            #img = cv2.resize(img, (400, 330))

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

