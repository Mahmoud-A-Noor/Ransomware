from Crypto.Cipher import AES
from Crypto import Random
import os

class E_File:
    def __init__(self,key):
        self.key = key
    
    def encrypt(self,filepath):
        iv = Random.new().read(16)
        c = AES.new(self.key,AES.MODE_OFB,iv)
        with open(filepath,'rb') as input:
            with open(filepath+".en",'wb') as output:
                output.write(c.encrypt(input.read()))
        
        os.remove(filepath)
        return iv
    
    def decrypt(self,iv,filepath):
        d = AES.new(self.key,AES.MODE_OFB,iv)
        with open(filepath+".en",'rb') as input:
            with open(filepath,'wb') as output:
                output.write(d.decrypt(input.read()))
        
        os.remove(filepath+".en")



key = input("the key : ")
padding = lambda s: s + ( 32 - len(s) % 32 ) * "*"
key = padding(key).encode("ascii")

ED = E_File(key)

iv = ED.encrypt(r"C:\Users\mahmo\desktop\test.docx")

choice = input("do you want to decrypt ? ")
if choice:
    ED.decrypt(iv,r"C:\Users\mahmo\desktop\test.docx")
        
    