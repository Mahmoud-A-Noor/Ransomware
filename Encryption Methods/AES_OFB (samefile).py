from Crypto.Cipher import AES
from Crypto import Random

key = input("the key : ")
padding = lambda s: s + ( 32 - len(s) % 32 ) * "*"
key = padding(key).encode("ascii")

def encrypt(key,output_file):
    block_size = AES.block_size
    with open(output_file,'rb+') as file:
        data = file.read(block_size)
        iv = Random.new().read(16)
        c= AES.new(key,AES.MODE_OFB,iv)
        while(data):
            file.seek(-len(data),1)
            file.write(c.encrypt(data))
            data = file.read(block_size)
        return [key,iv]
    
def decrypt(key,iv,output_file):
    block_size = AES.block_size
    with open(output_file,'rb+') as file:
        data = file.read(block_size)
        d = AES.new(key,AES.MODE_OFB,iv)
        while(data):
            file.seek(-len(data),1)
            file.write(d.decrypt(data))
            data = file.read(block_size)

# key = Random.new().read(16)
e = encrypt(key,r"C:\Users\mahmo\desktop\test.docx")
# print(e)
choice = input("do you want to decrypt ? ")
if choice:
    decrypt(e[0],e[1],r"C:\Users\mahmo\desktop\test.docx")