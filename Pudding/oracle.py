from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import base64
import json
import sys
import socket
import select
import threading
from thread import *

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
message = json.dumps({"username": "pudding_lover_1997", "password": "$up3r1337p4$$w0rd", "admin": 0, "flag": "BtS-CTF{et_tu_p4dd1ng?}"})
key = "mlkDSJFH89xcvmCD"
IV = "REALLY_NOT_AN_IV"

def main():
	establishConnection()
	listenAndCreateNewSession()
	return

def establishConnection():
	host = sys.argv[1] 
	port = int(sys.argv[2])
	socket.bind((host, port))
	return

def listenAndCreateNewSession():
	max_connections = 50
	while True:
		socket.listen(max_connections)
		clientSocket, addr = socket.accept()
		example = Oracle(key, IV, message, clientSocket, addr)
	return

class Oracle:
	def __init__(self, key, IV, message, clientSocket, addr):
		self.blockSize = 16
		self.key = key
		self.IV = IV
		self.message = message
		
		thread = threading.Thread(target=self.run, args=(clientSocket,addr))
		thread.daemon = True
		thread.start()

	def run(self, clientSocket, addr):
		aes = AES.new(self.key, AES.MODE_CBC, self.IV)
		padded = pad(self.message, self.blockSize)
		ciphertext = base64.b64encode(IV + aes.encrypt(padded))

		clientSocket.setblocking(0)
		clientSocket.send("Grab your cookie!\n" + ciphertext + "\nWanna give me one too?\n")
		while True:
			ready = select.select([clientSocket], [], [], 2)
			if ready[0]:
				data = clientSocket.recv(4096)
				clientSocket.send(self.isAdmin(data))
				break
		clientSocket.close()


	def isAdmin(self, userInput):
		try:
			userInput = base64.b64decode(userInput)
		except:
			return "Not base64\n"

		if len(userInput) % self.blockSize == 0:
			userIV = userInput[:self.blockSize]
			aes = AES.new(self.key, AES.MODE_CBC, userIV)
			decrypted = aes.decrypt(userInput[self.blockSize:])
			
			try:
				decrypted = unpad(decrypted, self.blockSize)
			except:
				return "Incorrect padding!\n"

			try:
				unserialized = json.loads(decrypted)
			except:
				return "Incorrect json\n"
                        unserial = ""
                        if "username" in unserialized:
                                unserial += "Username: " + unserialized["username"] + "\n"
                        if "password" in unserialized:
                                unserial += "Password: " + unserialized["password"] + "\n"
                        if "admin" in unserialized:
                                unserial += "Is admin?: " + str(unserialized["admin"]) + "\n"
                        return unserial
		else:
			return "Input is not correct ciphertext\n"

main()
