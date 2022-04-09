"""
CS 494P Project
IRC - Server Application
"""

import socket, select, Chatrooms    # TODO remove socket here as well.
from Chatrooms import IRC_Application, Chatroom

# Import rich

from rich.console import Console
from rich.theme import Theme
from rich.traceback import install
from rich.logging import RichHandler

import logging
import os
import json

from py2neo import Graph

from Commands import message_parse

from modules import User


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
    
    return log

# Rich Init
rich_init()

def connect(log):

    uri = "bolt://localhost:7687"
    user = "neo4j"
    graph_password = os.getenv('BrainDBPassword')
    try:
        graph = Graph(uri, auth=(user, graph_password))
    except:
        log.info("No Database Found\n")
        log.info("Start Database and press press any key to continue\n")
        input()
        
    return graph
        
        
# Graph init
    
connect(log)


# Globals
PORT_NUMBER = 5050
SOCKET_LIST = []   # Maintain a list of socket connections
CLIENTS = {}    # Maintain a dictionary of clients. The key is the socket, the value is the username
BUFFER_SIZE = 2048  # Define the maxiumum message buffer size
MAX_NUMBER_OF_CLIENTS = 10  # Maxmimum number of clients

irc_instance = IRC_Application()  # The object to handle the IRC side of things.
default_room = Chatroom(Chatrooms.DEFAULT_ROOM_NAME)    # creates a new default room
irc_instance.rooms[default_room.name] = default_room  # puts the new default room into the room dictionary


def irc_server(graph, log):
    # get the host information:
    host = socket.gethostname()
    port = PORT_NUMBER

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # the server socket instance
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))   # bind the host address and port to the socket on line above
    log.info(f"Server socket bound to {host}:{port}\n")

    #tell the server how many clients MAX to listen to:
    server_socket.listen(MAX_NUMBER_OF_CLIENTS)

    SOCKET_LIST.append(server_socket)

    while True:
        # Populate a list of sockets that have been read
        try:
        	read_sockets, write_sockets, err_sockets = select.select(SOCKET_LIST, [], [])
        except Exception as e:
        	log.info(e)
        for notified_socket in read_sockets:
            # Case where the server socket is being read from (i.e. initial client connection):
            # Add the client to the socket list and the client dictionary
            # and add the client to the default room
            if notified_socket == server_socket:

                new_client_socket, new_client_address = server_socket.accept()
                SOCKET_LIST.append(new_client_socket)
                log.info(f"New connection attempt from {new_client_address}\n")

                # The initial message data will be the username to add to the client dictionary
                user_pass = new_client_socket.recv(BUFFER_SIZE).decode()   
                
                user_pass = json.loads(user_pass)
                
                tmp_usr = User.User(user_pass, new_client_address)
                
                user = tmp_usr.name
                password = tmp_usr.password
                
                user_back = graph.run(f"MATCH (u: User) WHERE u.name = '{user}' RETURN (u)", user=user).evaluate()
                
                returned_pass = graph.run(f"MATCH (u: User) WHERE u.name = '{user}' RETURN u.password", user=user).evaluate()

                if user_back != None:
                	if password == returned_pass:
                	   
                		CLIENTS[new_client_socket] = user
                		new_client_socket.send(f"Welcome to the server, {user}\n".encode())
                		irc_instance.rooms[Chatrooms.DEFAULT_ROOM_NAME].add_new_client_to_chatroom(user, new_client_socket)
                	else:
                		new_client_socket.send(f"Password incorrect, please try again or contact system administrator".encode())
                		new_client_socket.close()
                		SOCKET_LIST.pop()
                		
                		
                else:
                	new_client_socket.send(f"Username {user} not found, please try again or contact system administrator".encode())
                	new_client_socket.close()
                	SOCKET_LIST.pop()
                	

            # Case where client socket is being read from:
            # Decode and handle the message
            else:
                message = notified_socket.recv(BUFFER_SIZE).decode()

                # If client disconnected, message will be empty
                # and client will be removed from socket list and client dictionary
                if not message:
                    notified_socket.close()

                    # TODO Remove client from all rooms
                    # THIS SEEMS TO WORK NOW! Tested!
                    for a_room in irc_instance.rooms:
                        if notified_socket in irc_instance.rooms[a_room].client_sockets:
                            irc_instance.rooms[a_room].remove_client_from_chatroom(CLIENTS[notified_socket], notified_socket)
                    
                    SOCKET_LIST.remove(notified_socket)
                    CLIENTS.pop(notified_socket)

                # Send the message to the parser to be handled
                else:
                    message_parse(irc_instance, notified_socket, user, message)

    server_socket.close()  # gracefully exit


if __name__ == '__main__':
    log = rich_init()
    graph = connect(log)
    irc_server(graph, log)
