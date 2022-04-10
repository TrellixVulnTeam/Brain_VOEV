
import socket

# Import rich

from rich.console import Console
from rich.theme import Theme
from rich.traceback import install
from rich.logging import RichHandler

import logging

import sys, errno


# Globals
DEFAULT_ROOM_NAME = '#default'


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

# Broadcast a message to the server and to all clients in that room
def message_broadcast(room, sender_name, sender_socket, message):
    log.info(f"{room.name}:{sender_name}> {message}")

    # Send the message to all clients except the one that sent the messaage
    for client_socket in room.client_sockets:
        if client_socket != sender_socket:
            try:
                client_socket.send(f"{room.name}:{sender_name}> {message}".encode())
            except IOError as io:
            	if io.errno == errno.EPIPE:
            		pass
            except Exception as e:
            	log.info('Failed to send message to client')
            	log.info(e)
                
                	


# The container that has rooms, which have lists of clients
class IRC_Application:
    def __init__(self):
        self.rooms = {}  # Create a dictionary of rooms with the room name as the key and the room object as the value

    # Function to create a space-separated list of rooms
    def list_all_rooms(self):
        room_list = ""
        for room in self.rooms.values():
            room_list = room_list + room.name + ' '
        room_list = room_list + '\n'
        return room_list


    # Check if the room name begins with '#', check if user is already in the room,
    # create the room if it does not exist, then join the room the user specified
    def join_room(self, room_to_join, sender_socket, sender_name):
        if room_to_join[0] != '#':
            sender_socket.send("Error: Room name must begin with a '#'\n".encode())
            return
        if room_to_join not in self.rooms:  # Assume that the room does not exist yet
            self.create_room(room_to_join, sender_socket, sender_name)
        else:  # otherwise, go through the room members to make sure that the sender is not in it already
            for current_members in self.rooms[room_to_join].client_sockets:
                if sender_socket == current_members:
                    sender_socket.send(f"Error: You are already in the room: {room_to_join}\n".encode())
                else:
                    # if we are here then the room exists and the sender is not in it.
                    self.rooms[room_to_join].add_new_client_to_chatroom(sender_name, sender_socket)

    # Create a new Chatroom, add the room to the room list, and add the client to the chatroom
    # A room cannot exist without a client, so one must be supplied
    def create_room(self, room_to_join, sender_socket, sender_name):
        new_room = Chatroom(room_to_join)
        self.rooms[room_to_join] = new_room
        self.rooms[room_to_join].add_new_client_to_chatroom(sender_name, sender_socket)

    # Check if the room exists, check if user is in the room,
    # remove user from room and delete room if it is empty
    def leave_room(self, room_to_leave, sender_socket, sender_name):
        if room_to_leave not in self.rooms:
            sender_socket.send("Error: Room does not exist\n".encode())
        elif sender_socket not in self.rooms[room_to_leave].client_sockets:
            sender_socket.send("Error: You are not in that room\n".encode())
        else:
            self.rooms[room_to_leave].remove_client_from_chatroom(sender_name, sender_socket)
            if not self.rooms[room_to_leave].client_sockets:
                self.rooms.pop(room_to_leave)

    # Check if rooms exist, check if user is in rooms,
    # if room exists and user is in it then send message, otherwise skip
    def message_rooms(self, rooms_to_send, sender_socket, sender_name, message):
        for room in rooms_to_send:
            if room not in self.rooms:
                sender_socket.send(f"Error: {room} room does not exist\n".encode())
                continue
            if sender_socket not in self.rooms[room].client_sockets:
                sender_socket.send(f"Error: You are not in the {room} room\n".encode())
                continue
            message_broadcast(self.rooms[room], sender_name, sender_socket, message)


class Chatroom:
    # Give a Chatroom a name and list of client's sockets in this room 
    def __init__(self, room_name):
        self.name = room_name
        self.client_sockets = []
        self.client_list = {}       # A dictionary of clients with sockets as the key and username as the value

    # Adds a new client to a chatroom and notifies clients in that room
    def add_new_client_to_chatroom(self, client_name, new_socket):
        self.client_sockets.append(new_socket)
        self.client_list[new_socket] = client_name
        message = f"{client_name} has joined the room.\n"
        message_broadcast(self, client_name, new_socket, message)

    # Removes an existing client from a chatroom and notifies the clients in that room
    def remove_client_from_chatroom(self, client_name, client_socket):
        self.client_sockets.remove(client_socket)
        self.client_list.pop(client_socket)
        message = f"{client_name} has left the room.\n"
        message_broadcast(self, client_name, client_socket, message)

    def list_clients_in_room(self):
        return list(self.client_list.values())
