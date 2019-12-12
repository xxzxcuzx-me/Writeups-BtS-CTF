from Crypto.Util.Padding import pad
import nclib
import base64
from os import urandom

#ip = "ctf.whitehats.pwr.edu.pl"
ip = "127.0.0.1"
#port = 30204
port = 4444

# najpopularniejszy rozmiar bloku
blockSize = 16
# tekst który chcemy zaszyfrować
textToForge = bytearray(pad('{"admin": 1}', blockSize))

# funkcja wykonująca zapytanie do wyroczni
def askOracle(question):
        flag = True
        while(flag):
                try:
                    flag = False
                    nc = nclib.Netcat(connect=(ip, port))
                    nc.recv_until("?\n")
                    nc.send(question)
                    response = nc.recv_all()
                    nc.close()
                    # zwróć informację, czy padding był prawidłowy
                    return "Incorrect padding!" not in response
                except Exception as inst:
                    print inst
                    flag = True

ciphertext = bytearray(urandom(blockSize))
i = len(textToForge)-blockSize
while i>=0:
	IV = bytearray(urandom(blockSize))
	for j in range(1, blockSize+1):
		for k in range(256):
                        # zmieniaj bajt w poprzednim bloku dopóki padding jest nieprawidłowy
			IV[blockSize - j] = k
			question = base64.b64encode(IV + ciphertext[:blockSize])
			if askOracle(question):
				intermediate = j ^ k 
				for l in range(1, j+1):
					IV[blockSize - l] = IV[blockSize - l] ^ j ^ (j+1)
				break
	for j in range(blockSize):
		IV[j] = IV[j] ^ (blockSize+1) ^ textToForge[i+j] # przygotuj blok szyfrogramu
	ciphertext = IV + ciphertext
	i-=blockSize

print base64.b64encode(ciphertext)
