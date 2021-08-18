from Crypto import PublicKey
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


key = RSA.generate(2048)
publicKey = key.publickey().exportKey()
privateKey = key.exportKey()

with open("c:/Users/mahmo/Desktop/publickey.txt",'w') as file:
    file.write(publicKey.decode('ascii'))
    
print(publicKey)

with open("c:/Users/mahmo/Desktop/privatekey.txt",'w') as file:
    file.write(privateKey.decode('ascii'))
    
print(privateKey)

