import mysql.connector as mysql
import db_infos

class DBCom():

	def connect(self):
		conn = mysql.connect(**db_infos.db_config)
		cursor = conn.cursor()
		return conn, cursor

	def selectDB(self, cursor):
		cursor.execute("USE ProjectM")

	def close(self, conn, cursor):
		cursor.close()
		conn.close()

	def add_user(self, username, password, email):
		conn, cursor = self.connect()
		self.selectDB(cursor)
		cursor.execute(
		"CALL add_user(%s,%s,%s)", (username, password, email)
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
		user_id = cursor.fetchall()[0][0]
		if user_id:
			cursor.execute(
			"SELECT password FROM Users WHERE id = %s", (user_id,))
			if password == cursor.fetchall()[0][0]:
				self.close(conn, cursor)
				return True
		self.close(conn, cursor)
		return False
