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


    while 1:
      print ("Waiting msg ...")
      msgServeur = mySocket.recv(1024).decode("Utf8")
      print("S>", msgServeur)
      if msgServeur.upper() == "VIDEO":
          msgClient = "VIDEORESP"
          mySocket.send(msgClient.encode("Utf8"))
          v = Thread(target  = VideoStream, args =(10, ))
          v.start()
      elif msgServeur.upper() == "VIDEOSTOP":
          msgClient = "VIDEORESPSTOP"
          mySocket.send(msgClient.encode("Utf8"))
          v.exit()
      elif msgServeur.upper() == "QUIT":
          msgClient = "QUITRESP"
          mySocket.send(msgClient.encode("Utf8"))
          mySocket.close()
          # 4) Fermeture de la connexion :
          print("Connexion interrompue.")
          break
      else :
          msgClient = input("C> ")
          mySocket.send(msgClient.encode("Utf8"))



print("Launching ...")
main()
print("Done.")
