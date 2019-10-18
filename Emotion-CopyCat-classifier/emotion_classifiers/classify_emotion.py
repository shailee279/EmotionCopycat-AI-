
import os
import cv2
import numpy as np

face_detector = None
face_detection_confidence = 0.5
# face_detector_folder = os.getcwd() + os.sep + 'face_detection_model'
face_detector_folder = 'emotion_classifiers/face_detection_model'

def print_stuff():
    print('....stuff.....')



# ------------------------------ Face Classification ---------------------
def init_models():
    print('init_models()...')
    load_face_detector()
    # load_emotion_classifier()


def load_face_detector():
    # load our serialized face detector from disk
    print("[INFO] loading face detector...")
    print('current dir: ', os.getcwd())
    protoPath = os.path.sep.join([face_detector_folder, "deploy.prototxt"])
    modelPath = os.path.sep.join([face_detector_folder,
        "res10_300x300_ssd_iter_140000.caffemodel"])
    # you need to specify that you are refering to the global variable, but not creating a new local variable
    global face_detector
    face_detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
    if face_detector is not None:
        print('[INFO] face detector loaded succesfully', face_detector)
    else: print('[OOPS!] face detector did not load :(')

def load_emotion_classifier():
    # Emotion list (the same list this FisherFace model was trained to recognise)
    emotions = ["neutral", "anger", "disgust", "fear", "happy", "sadness", "surprise"] 

def get_faces(frame):
    # a list of detected faces 
    detectedFaces = []

    # grab the image dimensions
    (h, w) = frame.shape[:2]
    # construct a blob from the image
    imageBlob = cv2.dnn.blobFromImage(
		cv2.resize(frame, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)
 
	# apply OpenCV's deep learning-based face detector to localize
	# faces in the input image
    face_detector.setInput(imageBlob)
    detections = face_detector.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
        confidence = detections[0, 0, i, 2]
 
        # filter out weak detections
        if confidence > face_detection_confidence:
            # compute the (x, y)-coordinates of the bounding box for
            # the face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # extract the face ROI
            face = frame[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
                continue

            # # count confidence in %
            # confidence *= 100
            # create faceDict for the list of dictionaries and append it to faces
            faceDict = {'face': face, 'confidence': confidence, 'bounds': (startX, startY, endX, endY), 'label': ""}
            detectedFaces.append(faceDict)
        return detectedFaces

def mark_faces_in_frame(frame):
    # find faces in the frame
    faces = get_faces(frame)

    for face in faces:
        # draw the bounding box of the face along with the
        # associated confidence
        name = "a face" if face['label'] == "" else face['label']
        text = "{}: {:.2f}%".format(name, face['confidence'])
        (startX, startY, endX, endY) = face['bounds']
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(frame, (startX, startY), (endX, endY),
            (0, 0, 255), 2)
        cv2.putText(frame, text, (startX, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    
    return frame

