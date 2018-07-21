import os
import sys
import errno
import socket
import select
import datetime

class ProjectM_Server():
	def __init__(self):
		self.server_address = ''
		self.server_port = 4242
		self.server_infos = (self.server_address, self.server_port)
		self.maxuptime = datetime.timedelta(seconds = 600)
		self.server_socket, self.online = self.start()
		self.starttime = datetime.datetime.now()
		print('Server online at ' + str(datetime.datetime.now()))
		self.user_list = []

	def start(self):
		"""Set the server online.
		Returns its socket and True if no errors occurs."""

		try:
			server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_socket.bind(self.server_infos)
			server_socket.listen(5)
		except OSError as err:
			if err.errno == os.errno.EADDRINUSE:
				print("Error : " + os.strerror(err.errno) + " (Port : " +
				str(self.server_infos[1]) + ")")
			sys.exit(1)
		return server_socket, True

	def mainloop(self):
		while (self.online and datetime.datetime.now() < (self.starttime + self.maxuptime)):
			#Checks for new connexion in queue every 50ms
			self.new_connexion, wlist, xlist = select.select([self.server_socket], [], [], 0.05)
			self.accept_connexion()
			#Listen to users
			if self.user_list != []:
				self.connectionCheck()
				try:
					self.to_read, wlist, xlist = select.select([u[0] for u in self.user_list],
					[], [], 0.05)
				except select.error as err:
					pass
				else:
					#Listen to users
					self.listen_user()
		#If the server reaches its maximum MAX_UPTIME
		#Close all sockets connected and finally close the server's socket
		if (self.online and datetime.datetime.now() > (self.starttime + self.maxuptime)):
			print("Closing all Clients socket.")
			for user in self.user_list:
				user[0].close()
			self.online = False

	def connectionCheck(self):
		for user in self.user_list:
			try:
				user[0].send('?PING\n'.encode())
			except:
				pass

	def accept_connexion(self):
		"""Accept newly logged users."""
		if self.new_connexion != []:
			for new_user in self.new_connexion:
				#Accepts newly logged user
				socket, infos = new_user.accept()
				print("New connection : " + str(infos))
				#Adds new user's socket to the list
				self.user_list.append([socket, infos, ''])

	def listen_user(self):
		"""Get users inputs."""
		for user in self.to_read:
			try:
				received = user.recv(1024)
			except ConnectionResetError as err:
				print("Error : " + os.strerror(err.errno))
				print(user)
				self.logout_user(user, True)
			else:
				if received.decode()[:8] == '?RENAME\n':
					for u in self.user_list:
						if u[0] == user:
							u[2] = received.decode()[8:]
				elif received.decode()[:9] == '?REQUEST\n':
					namelist = '?REQUEST\n'
					for u in self.user_list:
						namelist = namelist + u[2] + '\n'
					user.send(namelist.encode())
				elif received.decode() != "" and received.decode() != "\n":
					src = user
					for u in self.user_list:
						if u[0] == src:
							username = u[2]
					self.send_msg(received, src, username)

	def send_msg(self, msg, src, username):
		fullMsg = 'From ' + username + ' :\n\t' + msg.decode()
		fullMsg = fullMsg.encode()
		for user in self.user_list:
			if user[0] != src:
				user[0].send(fullMsg)

	def logout_user(self, user, forced):
		"""Logs out from the server the given user and notifies it,
		except if it's a forced disconnection."""
		i = 0
		while self.user_list[i][0] != user and i < len(self.user_list):
			i += 1
		print(str(self.user_list[i][1]) + " logged out. Closing socket.")
		if not forced:
			user.send(b"Logout\n")
		user.close()
		s = str(self.user_list[i][1]) + " disconnected.\n"
		del self.user_list[i]
		#Broadcast to all users someone disconnected
		for user in self.user_list:
			user[0].send(s.encode())

if __name__ == "__main__":
	pmServer = ProjectM_Server()
	pmServer.mainloop()
