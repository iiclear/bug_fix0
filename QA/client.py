#coding:utf8
import socket
import SocketServer

ip_port =('127.0.0.1',5001)
s = socket.socket()

s.connect(ip_port)

while True:
    data = s.recv(4096)
    print 'answer: ', data
    send_data = raw_input('>>: ').strip()
    s.send(send_data.encode('utf8'))
