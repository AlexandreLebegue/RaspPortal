# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket, sys, os
import sys
import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import face_recognition
import detection
import time
from gpiozero import Button
from gpiozero import LED

from threading import Thread


def VideoStream(duration) :
    print ("Starting Thread ...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8485))
    connection = client_socket.makefile('wb')

    cam = cv2.VideoCapture(0)

    cam.set(3, 320);
    cam.set(4, 240);

    img_counter = 0

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    start = time.time()
    timer = 0
    while timer < duration:
        ret, frame = cam.read()
        result, frame = cv2.imencode('.jpg', frame, encode_param)
    #    data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)


        #print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1
        timer = time.time() - start


    cam.release()
    client_socket.close()
    print("Quitting thread")


def main() :
    HOST = '127.0.0.1'
    PORT = 8585

    # 1) création du socket :
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) envoi d'une requête de connexion au serveur :
    try:
      mySocket.connect((HOST, PORT))
    except socket.error:
      print("La connexion a échoué.")
      sys.exit()
    print("Connexion établie avec le serveur.")

    # 3) Dialogue avec le serveur :
    video_stream = False


    #Facedetection Init

    YELLOPIN = 17
    REDPIN = 27
    GREENPIN = 22
    BUTTONPIN = 2



    print("Initialize")
    #Face Detection INIT
    cap = cv2.VideoCapture(0)

    alexandre_face = face_recognition.load_image_file("data/alexandre.jpeg")
    alexandre_face_encoding = face_recognition.face_encodings(alexandre_face)[0]

    sarah_face = face_recognition.load_image_file("data/sarah.jpg")
    sarah_face_encoding = face_recognition.face_encodings(sarah_face)[0]

    mama_face = face_recognition.load_image_file("data/maman.jpg")
    mama_face_encoding = face_recognition.face_encodings(mama_face)[0]

    papa_face = face_recognition.load_image_file("data/papa.jpg")
    papa_face_encoding = face_recognition.face_encodings(papa_face)[0]

    known_faces = [
        alexandre_face_encoding,
        sarah_face_encoding,
        mama_face_encoding,
        papa_face_encoding
    ]

    isFacedetected = False

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    frame_number = 0

    #GPIO INIT

    launchButton = Button(BUTTONPIN)
    yellowLed = LED(YELLOPIN)
    redLed = LED(REDPIN)
    greenLed = LED(GREENPIN)


    while 1:
        isFacedetected = False
        redLed.off()
        greenLed.off()
        yellowLed.off()
        print("Waiting button pressed ...")
        launchButton.wait_for_press() #attente passive... ?
        #input("enter to simulate press button")
        #Launching face detection
        yellowLed.on()
        redLed.off()
        greenLed.off()

        for i in range(5):
            result = detection.detect(known_faces, cap)
            if result[0]:
                isFacedetected = result[0]
                name = result[1]
        #End Of detection...

        #Treatement
        if isFacedetected:
            greenLed.on()
            print(name)
        else:
            redLed.on()
            v = Thread(target  = VideoStream, args =(10, ))
            v.start()
            msgClient = "VIDEO"
            mySocket.send(msgClient.encode("Utf8"))




print("Launching ...")
main()
print("Done.")
