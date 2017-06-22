import socket
import time
import threading
import sys
import os
import struct
import MessageUtil_pb2

writepath = './Input.bs'
readpath = './recv.bs'
temppath = './temp.bs'

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    sock.send(struct.pack('>I', len(msg)))
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #创建socket (AF_INET:IPv4, AF_INET6:IPv6) (SOCK_STREAM:面向流的TCP协议)

s.bind(('0.0.0.0', 10051))                           #绑定本机IP和任意端口(>1024)

s.listen(1)

print('Server is running...')                  
                               
def TCP(sock, addr):                                   
    
    print('Accept new connection from %s:%s.' %addr) 
    while True:
        data = recv_msg( sock )
        if data is None:
            sock.close()
            break
        #print( data ) # debug
        messageBox = MessageUtil_pb2.MessageBox()
        messageBox.ParseFromString( data )
        fp2 = open( writepath , "wb" )	
        fp2.write( data )
        fp2.close()
        if not data:
            break
        #sock.send( '咸柱'.encode( 'utf-8') );
        if messageBox.type is 4:
           newdata = recv_msg( sock )
           print( newdata ) # debug
           if newdata is None:
           		break
           fp3 = open( temppath , "wb" )
           fp3.write( newdata )
           fp3.close()
        time.sleep( 0.72 )
        while os.path.exists( readpath ) is False:
        	pass
        fp = open( readpath , "rb" )
        data = fp.read()
        fp.close()
        os.remove( readpath )
        if messageBox.type is 4:
        	os.remove( temppath )
        #print( data )
        send_msg( sock , data )
        break
    sock.close()
    print('Connection from %s:%s closed.' %addr)

while True:
    sock, addr = s.accept()
    TCP(sock, addr)