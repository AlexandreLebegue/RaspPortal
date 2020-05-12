import face_recognition
import cv2
from threading import Thread

class DetectThread(Thread):
    def __init__(self, known_faces):
        ''' Constructor. '''

        Thread.__init__(self)
        self.known_faces = known_faces
        self.frame = []

    def detect(self, frame):
        faceDetected = False
        name = ""
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame =   cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(self.known_faces, face_encoding, tolerance=0.50)

            # If you had more than 2 faces, you could make this logic a lot prettier
            # but I kept it simple for the demo
            name = None
            if match[0]:
                name = "Alexandre"
                faceDetected = True
            elif match[1]:
                name = "Sarah"
                faceDetected = True
            elif match[2]:
                name = "Mama"
                faceDetected = True
            elif match[3]:
                name = "Popa"
                faceDetected = True

            face_names.append(name)
        return faceDetected, name

    def run(self):
        while True:
            if len(self.frame) > 0:
                frametoDetect = self.frame[0]
                result = self.detect(frametoDetect)
                if result[0]:
                    isFacedetected = result[0]
                    name = result[1]
                    print("face : ", name)
                del self.frame[0]
