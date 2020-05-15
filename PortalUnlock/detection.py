import face_recognition
import cv2


def detect(known_faces, cap):
    faceDetected = False
    name = ""
    # Grab a single frame of video
    ret, frame = cap.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

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
