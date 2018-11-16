import mysql.connector as mysql
import db_infos
import bcrypt
import re

class DBCom():

	def __init__(self, client):
		self.client = client

	def connect(self):
		conn = mysql.connect(**db_infos.db_config)
		cursor = conn.cursor()
		return conn, cursor

	def selectDB(self, cursor):
		cursor.execute("USE ProjectM")

	def close(self, conn, cursor):
		cursor.close()
		conn.close()

	def add_user(self, username, salt, password, email):
		conn, cursor = self.connect()
		self.selectDB(cursor)
		cursor.execute(
		"CALL add_user(%s,%s,%s,%s)", (username, salt, password, email)
		)
		conn.commit()
		self.close(conn, cursor)

	def del_user(self, username):
		conn, cursor = self.connect()
		self.selectDB(cursor)
		cursor.execute(
		"CALL del_user(%s)", (username,)
		)
		conn.commit()
		self.close()

	def update_username(self, old_username, new_username):
		conn, cursor = self.connect()
		self.selectDB(cursor)
		cursor.execute(
		"CALL update_username(%s,%s)", (old_username, new_username)
		)
		cursor.commit()
		self.close()

	def update_password(self, username, new_password):
		conn, cursor = self.connect()
		self.selectDB(cursor)
		cursor.execute(
		"CALL update_password(%s,%s)", (username, new_password)
		)
		cursor.commit()
		self.close()

	def update_email(self, username, new_mail):
		conn, cursor = self.connect()
		self.selectDB(cursor)
		cursor.execute(
		"CALL update_email(%s,%s)", (username, new_mail)
		)
		cursor.commit()
		self.close()

	def identify(self, username, password):
		conn, cursor = self.connect()
		self.selectDB(cursor)
		cursor.execute(
		"SELECT id FROM Users WHERE username = %s", (username,))
		queryReturn = cursor.fetchall()
		user_id = None
		if len(queryReturn) == 1:
			user_id = queryReturn[0][0]
		if user_id:
			cursor.execute(
			"SELECT salt FROM Users WHERE id = %s", (user_id,))
			salt = cursor.fetchall()[0][0]
			cursor.execute(
			"SELECT password FROM Users WHERE id = %s", (user_id,))
			testedHash = bcrypt.hashpw(password.encode(), salt.encode())
			if testedHash.decode() == cursor.fetchall()[0][0]:
				self.close(conn, cursor)
				return True
		self.close(conn, cursor)
		return False

	def getUsernameList(self):
		conn, cursor = self.connect()
		self.selectDB(cursor)
		cursor.execute(
		"SELECT username FROM Users"
		)
		queryReturn = cursor.fetchall()
		self.close(conn, cursor)
		return queryReturn

	def getSaltList(self):
		conn, cursor = self.connect()
		self.selectDB(cursor)
		cursor.execute(
		"SELECT salt FROM Users"
		)
		queryReturn = cursor.fetchall()
		self.close(conn, cursor)
		return queryReturn

	def getMailList(self):
		conn, cursor = self.connect()
		self.selectDB(cursor)
		cursor.execute(
		"SELECT email FROM Users"
		)
		queryReturn = cursor.fetchall()
		self.close(conn, cursor)
		return queryReturn

	def checkUsername(self, username):
		check = True
		usernameList = self.getUsernameList()
		i = 0
		for usernameTuple in usernameList:
			usernameList[i] = usernameTuple[0]
			i += 1
		if not re.search(r"[A-Za-z0-9_-]{4,}", username):
			self.client.gui.errorLabel.config(text=self.client.gui.errorLabel['text'] +
			self.client.gui.res.badNameRegex)
			check = False
		for registered in usernameList:
			if registered == username:
				self.client.gui.errorLabel.config(text=self.client.gui.errorLabel['text'] +
				self.client.gui.res.nameTaken)
				check = False
		return check

	def checkSalt(self, salt):
		check = True
		saltList = self.getSaltList()
		i = 0
		for saltTuple in saltList:
			saltList[i] = saltTuple[0]
			i += 1
		for registered in saltList:
			print(registered)
			if registered == salt:
				check = False
		return check

	def checkMail(self, email):
		check = True
		emailList = self.getMailList()
		i = 0
		for mailTuple in emailList:
			emailList[i] = mailTuple[0]
			i += 1
		if not re.search(r"^[A-Za-z0-9\._-]+@{1}[A-Za-z]+\.{1}[a-z]{2,}$", email):
			self.client.gui.errorLabel.config(text=self.client.gui.errorLabel['text'] +
			self.client.gui.res.badMailRegex)
			check = False
		for registered in emailList:
			if registered == email:
				self.client.gui.errorLabel.config(text=self.client.gui.errorLabel['text'] +
				self.client.gui.res.mailTaken)
				check = False
		return check
