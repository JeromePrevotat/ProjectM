class User():
	def __init__(self, username, password, sock, infos):
		self.username = username
		self.password = password
		self.sock = sock
		self.infos = infos
		self.logged = False