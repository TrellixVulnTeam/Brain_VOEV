"""
CS 494P Project
IRC - Client Application
"""


import socket, select, sys, Server  # TODO remove socket since we do not use it here either
# from Server import BUFFER_SIZE TODO remove since we likely do not need this

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

    install()

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

# Graph Init

from modules import graph_init
username, graph = graph_init.main(log)

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

    # Send initial message to server with username
    server_socket.send(username.encode())

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
        return(log.info("Enter username:"), input(),
                HOST,
                PORT,
                server_socket)

    # Give the user a prompt for input
    def user_input(self):
        input()
        sys.stdout.flush()
    
    def io_loop(self):
        ...
