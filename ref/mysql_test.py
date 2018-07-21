import mysql.connector as mysql

import GuiDBConfig as guiConfig


class MySQL():
	GUIDB = 'GuiDB'

	def connect(self):
		conn = mysql.connect(**guiConfig.dbConfig)
		cursor = conn.cursor()
		return conn, cursor

	def close(self, conn, cursor):
		cursor.close()
		conn.close()

	def showDBs(self):
		conn, cursor = self.connect()
		cursor.execute("SHOW DATABASES")
		print(cursor)
		print(cursor.fetchall())
		self.close(cursor, conn)

	def createGuiDB(self):
		conn, cursor = self.connect()
		try:
			cursor.execute(
			"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'").format(MySQL.GUIDB)
		except mysql.Error as err:
			print("Failed to Create DB : " + str(err))
		self.close(cursor, conn)

	def dropGuiDB(self):
		conn, cursor = self.connect()
		try:
			cursor.execute("DROP DATABASE {}").format(MySQL.GUIDB)
		except mysql.Error as err:
			print("Failed to Drop DB : " + str(err))
		self.close(cursor, conn)

	def useGuiDB(self, cursor):
		cursor.execute("USE guidb")

	def createTables(self):
		#CONNECTS AND SELECT DB
		conn, cursor = self.connect()
		self.useGuiDB(cursor)

		#CREATE TABLES
		cursor.execute("CREATE TABLE IF NOT EXISTS Books (		\
			Book_ID INT NOT NULL AUTO_INCREMENT,				\
			Book_Title VARCHAR(25) NOT NULL,					\
			Book_Page INT NOT NULL,								\
			PRIMARY KEY(Book_ID)								\
			)													\
			ENGINE = INNODB")
		cursor.execute("CREATE TABLE IF NOT EXISTS Quotations (	\
			Quote_ID INT AUTO_INCREMENT,						\
			Quotation VARCHAR(250),								\
			Books_Book_ID INT,									\
			PRIMARY KEY (Quote_ID),								\
			FOREIGN KEY (Books_Book_ID)							\
				REFERENCES Books(Book_ID)						\
				ON DELETE CASCADE								\
			) ENGINE=INNODB")

		#CLOSE CONNECTION
		self.close(cursor, conn)

	def dropTables(self):
		conn, cursor = self.connect()
		self.useGuiDB(cursor)
		cursor.execute("DROP TABLE Quotations")
		cursor.execute("DROP TABLE Books")
		self.close(cursor, conn)

	def showTables(self):
		conn, cursor = self.connect()
		cursor.execute("SHOW TABLES FROM guidb")
		print(cursor.fetchall())
		self.close(cursor, conn)

	def insertBooks(self, title, page, bookQuote):
		conn, cursor = self.connect()
		self.useGuiDB(cursor)
		cursor.execute(
		"INSERT INTO Books(Book_Title, Book_Page)\
		VALUES (%s,%s)", (title,page))
		keyID = cursor.lastrowid
		cursor.execute(
		"INSERT INTO Quotations(Quotation, Books_Book_ID)\
		VALUES (%s, %s)", (bookQuote, keyID))
		conn.commit()
		self.close(cursor, conn)

	def insertBooksExample(self):
		conn, cursor = self.connect()
		self.useGuiDB(cursor)
		cursor.execute("INSERT INTO Books (Book_Title, Book_Page)\
		VALUES ('Design Patterns', 7)")
		keyID = cursor.lastrowid
		cursor.execute("INSERT INTO Quotations(Quotation, Books_Book_ID)\
		VALUES (%s, %s)", ('Programming to an Interface, not an Implementation', keyID))
		cursor.execute("INSERT INTO Books(Book_Title, Book_Page)\
		VALUES ('xUnit Test Patterns', 31)")
		keyID = cursor.lastrowid
		cursor.execute("INSERT INTO Quotations(Quotation, Books_Book_ID)\
		VALUES (%s, %s)",('Philosophy of Test Automation', keyID))
		conn.commit()
		self.close(cursor, conn)

	def showBooks(self):
		conn, cursor = self.connect()
		self.useGuiDB(cursor)
		cursor.execute("SELECT * FROM Books")
		allBooks = cursor.fetchall()
		print(allBooks)
		self.close(cursor, conn)
		return allBooks

	def showColumns(self):
		conn, cursor = self.connect()
		self.useGuiDB(cursor)
		cursor.execute("SHOW COLUMNS FROM Quotations")
		print(cursor.fetchall())
		print('\n Pretty Print:\n--------------')
		from pprint import pprint
		cursor.execute("SHOW COLUMNS FROM quotations")
		pprint(cursor.fetchall())
		self.close(cursor, conn)

	def showData(self):
		conn, cursor = self.connect()
		self.useGuiDB(cursor)
		cursor.execute("SELECT * FROM Books")
		print(cursor.fetchall())
		cursor.execute("SELECT * FROM Quotations")
		print(cursor.fetchall())
		self.close(cursor, conn)

	def showDataWithReturn(self):
		conn, cursor = self.connect()
		self.useGuiDB(cursor)
		cursor.execute("SELECT * FROM Books")
		booksData = cursor.fetchall()
		cursor.execute("SELECT * FROM Quotations")
		quoteData = cursor.fetchall()
		self.close(cursor, conn)
		for record in quoteData:
			print(record)
		return (booksData, quoteData)

	def updateGOF(self):
		conn, cursor = self.connect()
		self.useGuiDB(cursor)
		cursor.execute("SELECT Book_ID FROM Books WHERE Book_Title = 'Design Patterns'")
		primKey = cursor.fetchall()[0][0]
		print("Primary key=" + str(primKey))
		cursor.execute("SELECT * FROM quotations WHERE Books_Book_ID = (%s)", (primKey,))
		print(cursor.fetchall())
		cursor.execute("UPDATE Quotations SET Quotation = (%s)	\
		WHERE Books_Book_ID = (%s)",
		("Pythonic Duck Typing: If it walks like a duck and talks like a duck it probably is a duck...",
		primKey))
		conn.commit()
		cursor.execute("SELECT * FROM Quotations	\
		WHERE Books_Book_ID = (%s)", (primKey,))
		print(cursor.fetchall())
		self.close(cursor, conn)

	def deleteRecord(self):
		conn, cursor = self.connect()
		self.useGuiDB(cursor)
		cursor.execute("SELECT Book_ID FROM Books	\
		WHERE Book_Title = 'Design Patterns'")
		primKey = cursor.fetchall()[0][0]
		cursor.execute("DELETE FROM Books	\
		WHERE Book_ID = (%s)", (primKey,))
		conn.commit()
		self.close(cursor, conn)

if __name__ == "__main__":
	mySQL = MySQL()
	mySQL.deleteRecord()
	mySQL.showData()