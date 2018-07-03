from socket import *
import json
import os

HOST = "0.0.0.0" #local host
PORT = 7000 #open port 7000 for connection
s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1) #how many connections can it receive at one time
conn, addr = s.accept() #accept the connection
print "Connected by: " , addr #print the address of the person connected
while True:
    data = conn.recv(1024) #how many bytes of data will the server received
    if data != '':
        print "Received: ", repr(data)
        data = data[3:-1]
        f = open('gain.txt', 'w')
        f.write(data)
        f.close()
        L = data.split(',')
    if not data: 
    	break
conn.close()

os.execl('restart.sh', '')
