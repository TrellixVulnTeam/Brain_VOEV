from modules import view
from modules import create
from modules import update
from modules import create_task
from modules import tasks
from modules import complete_task
from modules import BrainAPI
from modules import attach
from modules import graph_init
from modules import login

# Import rich

from rich.console import Console
from rich.theme import Theme
from rich.traceback import install
from rich.logging import RichHandler
import logging

import Chatrooms
from Chatrooms import message_broadcast

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

def message_parse(self, sender_socket, sender_name, message):
        # Case where message is not a command:
        # The message is sent to the default channel
        if message[0] != '/':
            message_broadcast(self.rooms[DEFAULT_ROOM_NAME], sender_name, sender_socket, message)

        # Case where user wants to list all rooms:
        elif message.split()[0] == "/list" and len(message.split()) == 1:
            room_list = self.list_all_rooms()
            sender_socket.send(room_list.encode())

        # Case where user wants to join a room:
        elif message.split()[0] == "/join":
            if len(message.strip().split()) < 2:
                sender_socket.send(f"/join requires a #roomname argument.\nPlease enter: /join #roomname\n".encode())
            else:
                self.join_room(message.split()[1], sender_socket, sender_name)

        # Case where user wants to leave a room:
        elif message.split()[0] == "/leave":
            if len(message.strip().split()) < 2:
                sender_socket.send(f"/leave requires a #roomname argument.\nPlease enter: /leave #roomname\n".encode())
            else:
                room_to_leave = message.strip().split()[1]
                if room_to_leave[0] != "#":
                    sender_socket.send(f"/leave requires a #roomname argument to begin with '#'.\n".encode())
                else:
                    self.leave_room(room_to_leave, sender_socket, sender_name)

        # Case where user wants to send messages to rooms:
        # Parse the string for rooms and add rooms to a list
        # Pass the rest of the string along as the message
        elif message.split()[0] == "/send":
            rooms_to_send = []
            message_to_send = []
            convert_to_str = ""  # empty string to convert array into string
            # Add all the arguments beginning with # to a list of rooms
            if len(message) < 2:
                sender_socket.send(f"/send requires a #roomname(s) argument(s).\nPlease enter: /send #roomname(s)\n".encode())
            else:
                for word in message.split():
                    if word[0] == '#':
                        rooms_to_send.append(word)
                    elif word[0] == '/':
                        continue
                    else:   # Assume the message is the string after the last room
                        message_to_send.append(word)
                if rooms_to_send.count == 0:
                    sender_socket.send(f"/send at least one #roomname(s) argument(s).\nPlease enter: /send #roomname(s)\n".encode())
                else:
                    convert_to_str = ' '.join([str(word) for word in message_to_send])
                    convert_to_str = convert_to_str + '\n'

                    self.message_rooms(rooms_to_send, sender_socket, sender_name, convert_to_str)


        # list all members in a room
        elif message.split()[0] == "/members":
            if len(message.split()) != 2:
                sender_socket.send(f"/members requires a single #roomname argument.\nPlease enter: /members #roomname\n".encode())
            elif message.split()[1][0] != '#':
                sender_socket.send(f"Room names must begin with a #\n".encode())
            elif message.split()[1] not in self.rooms:
                sender_socket.send(f"That room does not exist.\n".encode())
            else:
                room_name = message.split()[1]
                client_list = self.rooms[room_name].list_clients_in_room()
                new_message = ' '.join(client_list)
                new_message = new_message + '\n'
                sender_socket.send(new_message.encode())

        elif message.split()[0] == "/quit":
            if len(message.split()) != 1:
                sender_socket.send(f"/quit takes no arguments\n".encode())
            else:
                sender_socket.shutdown(socket.SHUT_WR)
		
	# End pre-built commands
	# Template:
        # elif message.split()[0] == "/pm":
        
        elif message.split()[0] == "/view":
        	view.main(log, graph, journal_title, username)
        elif message.split()[0] == "/create":
        	create.main(log, graph, journal_title, date_format, username)
        elif message.split()[0] == "/update":
        	update.main(log, graph, journal_title, username)
        elif message.split()[0] == "/tasks":
        	tasks.main(log, graph, username)
        elif message.split()[0] == "/create task":
        	create_task.main(log, graph, journal_title, date_format, hour_min, username)
        elif message.split()[0] == "/complete task":
        	complete_task.main(log, graph, username)
        elif message.split()[0] == "/attach":
        	attach.main(log, graph, username)
        elif message.split()[0] == "/new user":
        	new_user.user(log, graph)
        	

