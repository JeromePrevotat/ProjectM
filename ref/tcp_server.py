from socketserver import BaseRequestHandler, TCPServer

class RequestHandler(BaseRequestHandler):
	def handle(self):
		print('Server connected to :', self.client_address)
		while(True):
			rsp = self.request.recv(512)
			if not rsp: break
			self.request.send(b'Server received :' + rsp)

def startServer():
	serv = TCPServer(('', 4242), RequestHandler)
	serv.serve_forever()