import nclib
import base64
from os import urandom

#ip = "ctf.whitehats.pwr.edu.pl"
ip = "127.0.0.1"
#port = 30203
port = 4444

blockSize = 16
encrypted = bytearray(base64.b64decode("UkVBTExZX05PVF9BTl9JVrRT7egK11hJOM+myjr/0/4uC/Es32G67vMt5u3GjdSEAJnuKT/GW8kEa4OAAiX+nfMJHvLMYgXRewLCKeh+VR1Nd6agt7eDMjL8DQPavgs5BvGd4H4uVZ+bwQ/2U/145a0QSSNIlq8oUQkgE0NJjy3L0AoZQKcqBocNUPbWYsAA"))

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
                    return "Incorrect padding!" not in response
                except Exception as inst:
                    print inst
                    flag = True

i = len(encrypted) - blockSize
plaintext = bytearray()
while i>0:
	IV = bytearray(urandom(blockSize))
	for j in range(1, blockSize + 1):
		for k in range(256):
			IV[blockSize - j] = k
			question = base64.b64encode(IV + encrypted[i:i+blockSize])
			if askOracle(question):
				intermediate = j ^ k
				decryptedByte = encrypted[i - j] ^ intermediate
				plaintext = bytearray([decryptedByte]) + plaintext
				print plaintext
				for l in range(1, j+1):
					IV[blockSize - l] = IV[blockSize - l] ^ j ^ (j+1)
				break
	i -= 16
