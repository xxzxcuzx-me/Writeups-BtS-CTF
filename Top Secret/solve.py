import base64
encrypted = bytearray(base64.b64decode("UkVBTExZX05PVF9BTl9JVv3ZsbUWsLosMxCvG3TNKkJBvKdJchuG9Ci0bwn2WWPF62MuvmBG23QN6+pOkf0DQpRgkjxuXrQy1nbLmIFVjt/FkikzOq9TMKWz1/gI2xYK"))

encrypted[64]=encrypted[64]^ord('"')^ord(')')
encrypted[65]=encrypted[65]^ord(',')^ord('.')
encrypted[67]=encrypted[67]^ord('"')^ord('(')
encrypted[73]=encrypted[73]^ord('"')^ord(')')
encrypted[74]=encrypted[74]^ord(':')^ord(';')
encrypted[76]=encrypted[76]^ord('1')^ord('"')

print base64.b64encode(encrypted)
