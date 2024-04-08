import socket 
import sys
import time
import hashlib
import os

# Code précedent utilisant le hashing 
def manage(choice, filename, host, port, data, t_file, s):
	#hash_data = hashlib.sha256(data).digest()
	#s.sendall(hash_data)
	s.send(data)
	#if(s.recv(1024) == b'retry'):
	#	print("retry recu")
	#	manage(choice, filename, host, port, data, t_file, s)

# Fonction envoi_fichier : Permet d'envoyer le fichier par segment pour l'écriture
def envoi_fichier(choice, filename, host, port):
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((host,port))
			s.send(choice.encode()) 
			time.sleep(1) # Sleep requis pour éviter la fusion des messages par socket
			s.send(filename.encode())
			time.sleep(1) # Sleep requis pour éviter la fusion des messages par socket
			size = os.path.getsize(filename)
			s.send(str(size).encode())
			# On reçoit l'offset pour savoir ou l'on doit commencer le fichier
			offset = s.recv(1024).decode()
			with open(filename,'rb') as t_file:
				t_file.seek(int(offset))
				# On boucle et envoi les données par block de 1024bits
				while True:
					data = t_file.read(1024)
					if not data:
						break
					manage(choice, filename, host, port, data, t_file, s)	
	except Exception as e:
		# Si une erreur survient on retente de se connecter et attends une réponse
		print("Waiting to reconnect..")
		envoi_fichier(choice, filename, host, port)
	
# Fonction lancement_fichier_adhoc : Permet d'envoyer le nom du fichier à éxécuter via tcp
def lancement_fichier_adhoc(choice, filename,host,port):
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((host,port))
			s.send(choice.encode())
			time.sleep(1) # Sleep requis pour éviter la fusion des messages par socket
			data = filename.encode()
			s.send(data)
	except Exception as e:
		print("Erreur : " + str(e))	

# Fonction lancement_fichier_bluetooth : Permet l'envoie du nom du fichier à éxécuter via bluetooth
def lancement_fichier_bluetooth(choice, filename,host,port):
	with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM,socket.BTPROTO_RFCOMM) as s:
		s.connect((host,port))
		s.send(choice.encode())
		data = filename.encode()
		s.send(data)

# adresse ip  	
host = sys.argv[1]
# adresse mac 
mac_host = sys.argv[2]
# port tcp 
port_tcp = int(sys.argv[3])
# port bluetooth
port_bluetooth = int(sys.argv[4])
# nom du fichier à envoyer au receveur
filename = input("File name : ")
# choix de l'utilisateur entre écrire ou éxecuter 
choice = input("Type w pour écriture, x pour éxécution : ")

if choice == 'w':
	print("Début d'écriture") 
	envoi_fichier(choice, filename, host, port_tcp)
	print("Fin d'écriture")
elif choice == 'x':
	connexion_type = input("Utiliser la connexion bluetooth ? (y) ")
	if connexion_type == 'y':
		print("Demande d'éxecution en bluetooth") 
		lancement_fichier_bluetooth(choice, filename, mac_host, port_bluetooth)
	else:
		print("Demande d'éxecution en tcp") 
		lancement_fichier_adhoc(choice, filename, host, port_tcp)

