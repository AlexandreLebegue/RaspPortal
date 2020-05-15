# Définition d'un serveur réseau rudimentaire
# Ce serveur attend la connexion d'un client
# cd Documents/Developpement/Git/RaspPortail/PortalUnlock
# python -m server_test.py

import socket, sys
import cv2
import io
import socket
import struct
import time
import pickle
import zlib

from threading import Thread
import time

def VideoStream(duration):
    print ("Starting Thread ...")
    HOST=''
    PORT=8485

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST,PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')

    conn,addr=s.accept()

    data = b""
    payload_size = struct.calcsize(">L")
    #print("payload_size: {}".format(payload_size))
    start = time.time()
    timer = 0

    cv2.namedWindow("imgawindow", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("imgawindow",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    while timer < duration:
        while len(data) < payload_size:
            #print("Recv: {}".format(len(data)))
            data += conn.recv(4096)

        #print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        #print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow('imgawindow',frame)
        cv2.waitKey(1)
        timer = time.time() - start

    cv2.destroyWindow("imgawindow")

    s.close()
    print("Quitting thread")


def main():
    HOST = '127.0.0.1'
    PORT = 8585
    counter =0	 # compteur de connexions actives
    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    img = cv2.imread('fond_ecran.jpg',0)
    cv2.imshow('window',img)
    cv2.waitKey(1)

    # 1) création du socket :
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) liaison du socket à une adresse précise :
    try:
      mySocket.bind((HOST, PORT))
    except socket.error:
      print("La liaison du socket à l'adresse choisie a échoué.")
      sys.exit


    # 3) Attente de la requête de connexion d'un client :
    print("Serveur prêt, en attente de requêtes ...")
    mySocket.listen(5)

    # 4) Etablissement de la connexion :
    connexion, adresse = mySocket.accept()
    counter +=1
    print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))

    # 5) Dialogue avec le client :
    msgServeur ="VIDEO"
    connexion.send(msgServeur.encode("Utf8"))


    while 1:
        print ("Waiting msg ...")
        msgClient = connexion.recv(1024).decode("Utf8")
        print("C>", msgClient)
        if msgClient.upper() == "VIDEORESP":
            v = Thread(target  = VideoStream, args =(10, ))
            v.start()
        elif msgClient.upper() == "VIDEORESPSTOP":
            v.exit()
        elif msgClient.upper() == "QUITRESP":
            print("Connexion interrompue.")
            connexion.close()
            break

        msgServeur = input("S> ")
        connexion.send(msgServeur.encode("Utf8"))




print("Launching ...")
main()
print("Done.")
