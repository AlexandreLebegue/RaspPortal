# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket, sys, os
import sys
from  video_client import video_client_thread

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
v = video_client_thread()
video_stream = False


while 1:
  print ("Waiting msg ...")
  msgServeur = mySocket.recv(1024).decode("Utf8")
  print("S>", msgServeur)
  if msgServeur.upper() == "VIDEO":
      msgClient = "VIDEORESP"
      mySocket.send(msgClient.encode("Utf8"))

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

print("END.")
