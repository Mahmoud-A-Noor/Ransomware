from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter

def encryption(key,filepath):
    counter = Counter.new(128)
    c= AES.new(key,AES.MODE_CTR,counter = counter)
    
    with open(filepath,'rb+') as file:
        block_size = 16
        data = file.read(block_size)
        
        while data:
            file.seek(-len(data),1)
            file.write(c.encrypt(data))
            data = file.read(block_size)
        return key
    
def decryption(key,filepath):
    counter = Counter.new(128)
    c= AES.new(key,AES.MODE_CTR,counter = counter)
    
    with open(filepath,'rb+') as file:
        block_size = 16
        data = file.read(block_size)
        
        while data:
            file.seek(-len(data),1)
            file.write(c.decrypt(data))
            data = file.read(block_size)

key = Random.new().read(16)

e = encryption(key,r"C:\Users\mahmo\desktop\test.docx")
print(e)

choice = input("do you want to decrypt : ")
if choice:
    decryption(e,r"C:\Users\mahmo\desktop\test.docx")
