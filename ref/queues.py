from socket import socket, AF_INET, SOCK_STREAM

def writeToScroll(inst):
	print('Hi from Queue !')
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect(('localhost', 4242))
	for idx in range(10):
		sock.send(b'Message from a Queue ' + bytes(str(idx).encode()))
		recv = sock.recv(8192).decode()
		inst.guiQueue.put(recv)
	inst.createThread(6)