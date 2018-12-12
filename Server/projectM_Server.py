"""ProjectM Server Module."""

import os
import sys
import errno
import socket
import select
import datetime

import encoding

class ProjectM_Server():
    """ProjectM Server Class."""
    def __init__(self):
        self.server_address = ''
        self.server_port = 4242
        self.server_infos = (self.server_address, self.server_port)
        self.maxuptime = datetime.timedelta(seconds=600)
        self.server_socket, self.online = self.start()
        self.starttime = datetime.datetime.now()
        print('Server online at ' + str(datetime.datetime.now()))
        self.user_list = []
        self.to_read = None
        self.new_connexion = None

    def start(self):
        """Set the server online.
        Returns its socket and True if no errors occurs."""

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(self.server_infos)
            server_socket.listen(5)
        except OSError as err:
            if err.errno == os.errno.EADDRINUSE:
                print("Error : " + os.strerror(err.errno) + " (Port : " + \
                str(self.server_infos[1]) + ")")
            sys.exit(1)
        return server_socket, True

    def mainloop(self):
        """Server mainloop."""
        while (self.online and datetime.datetime.now() < (self.starttime + self.maxuptime)):
            #Checks for new connexion in queue every 50ms
            self.new_connexion, wlist, xlist = select.select([self.server_socket], [], [], 0.05)
            self.accept_connexion()
            #Listen to users
            if self.user_list != []:
                self.connection_check()
                try:
                    self.to_read, wlist, xlist = select.select([u[0] for u in self.user_list], \
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

    def connection_check(self):
        """Check if a connection to a Client has been lost."""
        cmd = encoding.encode_cmd("ping()")
        for user in self.user_list:
            try:
                user[0].send(cmd)
            except:
                pass

    def accept_connexion(self):
        """Accept newly logged users."""
        if self.new_connexion != []:
            for new_user in self.new_connexion:
                #Accepts newly logged user
                sock, infos = new_user.accept()
                print("New connection : " + str(infos))
                #Adds new user's socket to the list
                self.user_list.append([sock, infos, ''])

    def listen_user(self):
        """Get users inputs."""
        for user in self.to_read:
            try:
                received = user.recv(1024).decode()
            except ConnectionResetError as err:
                print("Error : " + os.strerror(err.errno))
                print(user)
                self.logout_user(user, True)
            else:
                #Loop to empty the buffer
                while received != "":
                    cmd, args, msg, length = encoding.parse_type_received(received)
                    #Commands
                    if cmd:
                        if cmd == "rename" and args != "":
                            for usr in self.user_list:
                                if usr[0] == user:
                                    usr[2] = args
                        elif cmd == "request":
                            namelist = "request("
                            for usr in self.user_list:
                                namelist = namelist + usr[2] + '\n'
                            namelist = namelist + ")"
                            user.send(encoding.encode_cmd(namelist))
                    #Messages
                    if not cmd:
                        src = user
                        for usr in self.user_list:
                            if usr[0] == src:
                                username = usr[2]
                        self.send_msg(msg, src, username)
                    received = received[length:]

    def send_msg(self, msg, src, username):
        """Send a received Message to all other connected Users."""
        full_msg = 'From ' + username + ' :\n\t' + msg
        for user in self.user_list:
            if user[0] != src:
                user[0].send(encoding.encode_msg(full_msg))

    def logout_user(self, user, forced):
        """Logs out from the server the given user and notifies it,
        except if it's a forced disconnection."""
        i = 0
        while self.user_list[i][0] != user and i < len(self.user_list):
            i += 1
        print(str(self.user_list[i][1]) + " logged out. Closing socket.")
        if not forced:
            user.send(encoding.encode_msg("Logout\n"))
        user.close()
        msg = str(self.user_list[i][2]) + " disconnected.\n"
        del self.user_list[i]
        #Broadcast to all users someone disconnected
        for usr in self.user_list:
            usr[0].send(encoding.encode_msg(msg))

if __name__ == "__main__":
    PMSERVER = ProjectM_Server()
    PMSERVER.mainloop()
