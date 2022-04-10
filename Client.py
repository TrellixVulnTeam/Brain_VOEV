"""
CS 494P Project
IRC - Client Application
"""


import socket, select, sys, Server  # TODO remove socket since we do not use it here either
# from Server import BUFFER_SIZE TODO remove since we likely do not need this

import getpass
import json

# Import rich

from rich.console import Console
from rich.theme import Theme
from rich.traceback import install
from rich.logging import RichHandler

import logging

# Define the host IP and port for the server
HOST = socket.gethostname()
PORT = 5050


def rich_init():

    install(show_locals=True)

    global console
    console = Console(record=True)
    custom_theme = Theme({"1": "red"})
    console = Console(theme=custom_theme)

    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    global log
    log = logging.getLogger("rich")

# Rich Init
rich_init()

# Ask For initial username and password

log.info("Username?")
username = input(">")

log.info("Password?")
password = getpass.getpass(f"{username}> ")

# Give the user a prompt for input
def user_input(username):
    input(f"{username}> ")
    sys.stdout.flush()


def irc_client(username):
    # Get the host IP and port for the server
    host = socket.gethostname()
    port = 5050
    
    # Create the server socket and connect to the server
    server_socket = socket.socket()
    server_socket.connect((host, port))
    log.info(f"Connected to server at {host}:{port}")

    # Send initial message to server with username and pass
    
    user_pass = [username, password]
    user_pass = json.dumps(user_pass)
    
    server_socket.send(user_pass.encode())

    # Loop to receive and send messages
    while True:
        # Check stdin for messages from the client and check the server socket for messages from the server
        socket_list = [sys.stdin, server_socket]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        # Handle each socket that is read from
        for notified_socket in read_sockets:

            # Handle message from server
            if notified_socket == server_socket:
                message = server_socket.recv(Server.BUFFER_SIZE).decode()
                # If server shuts down, recv will return an empty string
                if not message:
                    server_socket.shutdown(2)
                    server_socket.close()
                    log.info("\rDisconnected from the server")
                    sys.exit()
                # Erase the current line, then print the received message
                log.info('\r')
                sys.stdout.flush()
                
                
                if message.split()[0] == "return":
                	log.info(message.split(' ', 1)[1])
                	log.info(message)
                	
                	return_msg = input("Returning> ")
                	
                	server_socket.send(return_msg.encode)
                	
                else:
                	log.info(message)
                

            # Handle input from user
            else:
                message = (input(f"{username}> ") + "\n")
                server_socket.send(message.encode())
                

    server_socket.close()   # close connection


if __name__ == "__main__":
    irc_client(username)

class Client:
    def __init__(self, name, host, port, server_socket):
        self.name = name
        self.host = host
        self.port = port
        self.server_socket = server_socket
    
    @classmethod
    def from_input(cls, server_socket):
        return( HOST,
                PORT,
                server_socket)

    # Give the user a prompt for input
    def user_input(self):
        input()
        sys.stdout.flush()
    
    def io_loop(self):
        ...
