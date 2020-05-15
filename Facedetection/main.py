import face_recognition
import cv2
import detection
import time
from gpiozero import Button
from gpiozero import LED


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



print("Launch")

while True:
    isFacedetected = False
    redLed.off()
    greenLed.off()
    yellowLed.off()
    print("Waiting button pressed ...")
    launchButton.wait_for_press() #attente passive... ?
    #input("enter to simulate press button")
    print("Button pressed, launching detection ...")

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

    time.sleep(3)
