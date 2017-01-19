#!/usr/bin/env python

import socket,os,sys,errno,select

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

serverSocket.bind(("0.0.0.0",8000))
#why cant use 80? not allowed to use under 1200 port unless you have root
serverSocket.listen(5)


while True:
    (incomingSocket,address) = serverSocket.accept()
    #reaped = os.waitpid(0,os.WNOHANG)
    try:
	reaped = os.waitpid(0,os.WNOHANG)
	#print "Reaped %s" % (repr(reaped))
    except OSError, e:
	if e.errno == errno.ECHILD:
	    pass
	else:
	    raise
    else:
	print "Reaped %s" % (repr(reaped))
    
    print "Got a connection from %s" %(repr(address))
    
    
    if (os.fork() != 0):
	continue
    
    
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #AF_INET means we want an IPV4 socket
    #SOCK_STREAM means we want a TCP socket
    
    clientSocket.connect(("www.google.com",80))    
    incomingSocket.setblocking(0)
    clientSocket.setblocking(0)
    while True:
	request = bytearray()
	while True:
	    try:
		part = incomingSocket.recv(1024)
	    except IOError,e:
		if e.errno == socket.errno.EAGAIN:
		    break
		else:
		    raise
	    if (part):
		request.extend(part)
		clientSocket.sendall(part)
	    else:
		sys.exit(0) #quit the program
	
	if len(request) >0:
	    print (request)
	#=====================
	response = bytearray()  

	while True:
	    try:
		part = clientSocket.recv(1024)
	    except IOError, e:
		if e.errno == socket.errno.EAGAIN:
		    break
		else:
		    raise
	    if (part):
		response.extend(part)
		incomingSocket.sendall(part)
	    else:
		sys.exit(0) #quit the program    
	
	if len(response) >0:
	    print (response)
	select.select(
	    [incomingSocket,clientSocket],#read
	    [],                           #write
	    [incomingSocket,clientSocket],#exception
	    1.0)                          #timeout