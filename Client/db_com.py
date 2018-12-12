"""Module to communicate with the ProjectM Database."""

import re
import mysql.connector as mysql

import bcrypt
import db_infos

class DBCom():
    """Class to communicate with the Database."""
    def __init__(self, client):
        self.client = client

    def connect(self):
        """Connect to MySQL Server."""
        conn = mysql.connect(**db_infos.db_config)
        cursor = conn.cursor()
        return conn, cursor

    def select_db(self, cursor):
        """Select the ProjectM Database."""
        cursor.execute("USE ProjectM")

    def close(self, conn, cursor):
        """Stop Communiction with the Database."""
        cursor.close()
        conn.close()

    def add_user(self, username, salt, password, email, phone_number):
        """Add a new User to the Database."""
        conn, cursor = self.connect()
        self.select_db(cursor)
        cursor.execute("CALL add_user(%s,%s,%s,%s,%s)", \
        (username, salt, password, email, phone_number))
        conn.commit()
        self.close(conn, cursor)

    def del_user(self, username):
        """Delete an User from the Database."""
        conn, cursor = self.connect()
        self.select_db(cursor)
        cursor.execute("CALL del_user(%s)", (username,))
        conn.commit()
        self.close(conn, cursor)

    def update_username(self, old_username, new_username):
        """Update the Username of a given User."""
        conn, cursor = self.connect()
        self.select_db(cursor)
        cursor.execute("CALL update_username(%s,%s)", (old_username, new_username))
        conn.commit()
        #cursor.commit()
        self.close(conn, cursor)

    def update_password(self, username, new_salt, new_password):
        """Update the Password of a given User."""
        conn, cursor = self.connect()
        self.select_db(cursor)
        cursor.execute("CALL update_password(%s,%s,%s)", (username, new_salt, new_password))
        conn.commit()
        #cursor.commit()
        self.close(conn, cursor)

    def update_email(self, username, new_mail):
        """Update the Mail of a given User."""
        conn, cursor = self.connect()
        self.select_db(cursor)
        cursor.execute("CALL update_email(%s,%s)", (username, new_mail))
        cursor.commit()
        self.close(conn, cursor)

    def identify(self, username, password):
        """Try to Identify via an Username/Password Combo."""
        conn, cursor = self.connect()
        self.select_db(cursor)
        cursor.execute("SELECT id FROM Users WHERE username = %s", (username,))
        query_return = cursor.fetchall()
        user_id = None
        if len(query_return) == 1:
            user_id = query_return[0][0]
        if user_id:
            cursor.execute("SELECT salt FROM Users WHERE id = %s", (user_id,))
            salt = cursor.fetchall()[0][0]
            cursor.execute("SELECT password FROM Users WHERE id = %s", (user_id,))
            tested_hash = bcrypt.hashpw(password.encode(), salt.encode())
            if tested_hash.decode() == cursor.fetchall()[0][0]:
                self.close(conn, cursor)
                return True
        self.close(conn, cursor)
        return False

    def get_username_list(self):
        """Returns all the Username in the Database."""
        conn, cursor = self.connect()
        self.select_db(cursor)
        cursor.execute("SELECT username FROM Users")
        query_return = cursor.fetchall()
        self.close(conn, cursor)
        return query_return

    def get_salt_list(self):
        """Returns all the Salt in the Database."""
        conn, cursor = self.connect()
        self.select_db(cursor)
        cursor.execute("SELECT salt FROM Users")
        query_return = cursor.fetchall()
        self.close(conn, cursor)
        return query_return

    def get_mail_list(self):
        """Returns all the Mail in the Database."""
        conn, cursor = self.connect()
        self.select_db(cursor)
        cursor.execute("SELECT email FROM Users")
        query_return = cursor.fetchall()
        self.close(conn, cursor)
        return query_return

    def get_phone_number_list(self):
        """Returns all the Phone Number in the Database."""
        conn, cursor = self.connect()
        self.select_db(cursor)
        cursor.execute("SELECT phone_number FROM Users")
        query_return = cursor.fetchall()
        self.close(conn, cursor)
        return query_return

    def check_username(self, username):
        """Checks if an Username is Valid."""
        self.client.gui.error_label.config(text='')
        check = True
        username_list = self.get_username_list()
        i = 0
        for username_tuple in username_list:
            username_list[i] = username_tuple[0]
            i += 1
        if not re.search(r"[A-Za-z0-9_-]{4,}", username):
            self.client.gui.error_label.config(text=self.client.gui.error_label['text'] + \
            self.client.gui.res.bad_name_regex)
            check = False
        for registered in username_list:
            if registered == username:
                self.client.gui.error_label.config(text=self.client.gui.error_label['text'] + \
                self.client.gui.res.name_taken)
                check = False
        return check

    def check_salt(self, salt):
        """Checks if a Salt is Unique."""
        check = True
        salt_list = self.get_salt_list()
        i = 0
        for salt_tuple in salt_list:
            salt_list[i] = salt_tuple[0]
            i += 1
        for registered in salt_list:
            if registered == salt:
                check = False
        return check

    def check_mail(self, email):
        """Checks if a Mail is Valid."""
        self.client.gui.error_label.config(text='')
        check = True
        email_list = self.get_mail_list()
        i = 0
        for mail_tuple in email_list:
            email_list[i] = mail_tuple[0]
            i += 1
        if not re.search(r"^[A-Za-z0-9\._-]+@{1}[A-Za-z]+\.{1}[a-z]{2,}$", email):
            self.client.gui.error_label.config(text=self.client.gui.error_label['text'] + \
            self.client.gui.res.bad_mail_regex)
            check = False
        for registered in email_list:
            if registered == email:
                self.client.gui.error_label.config(text=self.client.gui.error_label['text'] + \
                self.client.gui.res.mail_taken)
                check = False
        return check

    def check_phone_number(self, phone_number):
        """Checks if a Phone Number is Valid."""
        self.client.gui.error_label.config(text='')
        check = True
        phone_number_list = self.get_phone_number_list()
        i = 0
        for phone_number_tuple in phone_number_list:
            phone_number_list[i] = phone_number_tuple[0]
            i += 1
        if not re.search(r"^\+{1}[0-9]{2}[0-9]{9}$", phone_number):
            self.client.gui.error_label.config(text=self.client.gui.error_label['text'] + \
            self.client.gui.res.bad_phone_number_regex)
            check = False
        for registered in phone_number_list:
            if registered == phone_number:
                self.client.gui.error_label.config(text=self.client.gui.error_label['text'] + \
                self.client.gui.res.phone_number_taken)
                check = False
        return check
