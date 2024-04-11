import socket
import subprocess
import sys
import bluetooth
import threading
import time
import hashlib
import os


### FICHIER POUR SERVEUR VERSION FINALE AVEC WIFI ET BLUETOOTH ###


#Numero du port sur lequel on va ecouter
port = int(sys.argv[1])	

##Fonction recv_file : Fonction qui gere la reception des fichiers
## Paramètres : - Conn, socket de la connection avec le client
##				- offset, variable pour savoir d'ou il faut commencer l'envoi
## retourne : - 0 si l'execution se passe normalement
##			  - Offset si il y'a une interruption lors de l'execution
def recv_file(conn,offset):
	# Recevoir les données
	filename = str(conn.recv(1024).decode())
	filesize = str(conn.recv(1024).decode())
	print("je recois le fichier:", filename)
	
	#jenvoie l'offset
	conn.send(str(offset).encode())
	with open(filename,'wb') as file :		
		while True:
			file.seek(offset)
			try:
				#Reception du hash de l'envoi
				#hash_recu = conn.recv(32) 
				#if not hash_recu:
					#break
					
				#Reception du contenu du fichier
				data = conn.recv(1024)
				if not data :
					break
					
				offset += len(data)
	
				#Verification des hash
				#hash_calculated = hashlib.sha256(data).digest()
				#if hash_calculated != hash_recu:
					#conn.send(b'retry')
					#continue
				#else:
					#conn.send(b'good')

				
				
				try:
					file.write(data)
					file.flush()
				except Exception as e:
					print("Erreur",e)
			
				
			except Exception as e :
				print("Erreur de reception des données:",e)
				
				return offset
				
	conn.close()
	print("Fin d'écriture")
	return 0
	


##Fonction start_bluetooth_server : Fonction pour lancer un serveur qui ecoute les connections sur bluetooth 
def start_bluetooth_server():
	server_bluetooth = socket.socket(socket.AF_BLUETOOTH,socket.SOCK_STREAM,socket.BTPROTO_RFCOMM)
	#Liaison du socket
	server_bluetooth.bind(('B8:27:EB:C9:02:3B',1))
	server_bluetooth.listen(3)
	
	#Gestion de l'ordre d'execution de fichier
	while True:
		conn, addr = server_bluetooth.accept()
		print('Connecté a :', addr)
		received = conn.recv(1024).decode()
		if received == "x":
			print("Execution en bluetooth")
			execute_file(conn)

	
	
##Fonction start_wifi_server : Fonction pour lancer un serveur qui ecoute les connections sur wifi
def start_wifi_server():	
	server_wifi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_wifi.bind(('',port))
	server_wifi.listen(3)
	offset = 0
	
	try:
		while True:
			conn, addr = server_wifi.accept()
			print('Connecté a :', addr)
			received = conn.recv(1024).decode()
			#Gestion de l'ordre d'ecriture de fichier
			if received == "w":
				offset=recv_file(conn,offset)
			#Gestion de l'ordre d'execution de fichier
			if received == "x":
				print("Execution en wifi")
				execute_file(conn)
	except Exception as e:
		print(e)


##Fonction recv_file : Fonction pour executer un fichier
## Paramètres : - Conn, socket de la connection avec le client
##		

def execute_file(conn):
	# Recevoir les données
	data = conn.recv(1024).decode()
	if not data :
		return
	print("Execution du fichier", data)
	subprocess.run(["bash",data])		
	conn.close()




##Fonction recv_file : Fonction main ou on lance le serveur wifi et le serveur bluetooth avec les threads
def main():
	
	print("En attente de connexion")
	
	threading.Thread(target=start_wifi_server,args=()).start()
	threading.Thread(target=start_bluetooth_server,args=()).start()





main()
