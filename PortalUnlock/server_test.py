# Définition d'un serveur réseau rudimentaire
# Ce serveur attend la connexion d'un client

import socket, sys
from  video_server import video_server_thread

HOST = '127.0.0.1'
PORT = 8585
counter =0	 # compteur de connexions actives

# 1) création du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2) liaison du socket à une adresse précise :
try:
  mySocket.bind((HOST, PORT))
except socket.error:
  print("La liaison du socket à l'adresse choisie a échoué.")
  sys.exit

while 1:
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
  v = video_server_thread()
  while 1:
    print ("Waiting msg ...")
    msgClient = connexion.recv(1024).decode("Utf8")
    print("C>", msgClient)
    if msgClient.upper() == "VIDEORESP":
        v.start()
    elif msgClient.upper() == "VIDEORESPSTOP":
        v.exit()
    elif msgClient.upper() == "QUITRESP":
        print("Connexion interrompue.")
        connexion.close()
        break

    msgServeur = input("S> ")
    connexion.send(msgServeur.encode("Utf8"))

Print("END.")
