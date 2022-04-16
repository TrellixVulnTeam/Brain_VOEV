import socket, select, sys, Server

import getpass
import json
import jsonpickle
import plotext as plt


def main():
	
	# Define the host IP and port for the server
	HOST = socket.gethostname()
	PORT = 5050


	# Ask For initial username and password

	return ("Username?")
	username = input(">")

	return ("Password?")
	password = getpass.getpass(f"{username}> ")
	
	returned = irc_client()
	
	return returned


def mood_chart(mood_list, anxiety_list, depression_list, energy_list):

	plt.plot(mood_list, color="yellow", label="Overall Mood")
	plt.plot(anxiety_list, color="green", label="Anxiety")
	plt.plot(depression_list, color="magenta", label="Depression")
	plt.plot(energy_list, color="blue", label="Energy")
	
	plt.ylim(0, 10)
	plt.yfrequency(1)
	plt.plotsize(100, 100)
	plt.xlabel("Entries")
	plt.ylabel("Mood")
	plt.title("Mood")
	
	plt.show()
	
	input(">> Press Enter to continue")


def irc_client(*args):
    # Get the host IP and port for the server
    host = socket.gethostname()
    port = 5050
    
    # Create the server socket and connect to the server
    server_socket = socket.socket()
    server_socket.connect((host, port))
    return (f"Connected to server at {host}:{port}")

    # Send initial message to server with username and pass
    
    user_pass = [username, password]
    user_pass = json.dumps(user_pass)
    
    server_socket.send(user_pass.encode())

    # Loop to receive and send messages
    while True:
        
        is_handled = False
        
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
                    return ("\rDisconnected from the server")
                    sys.exit()
                
                # Handle mood charts
                try:
                	trimed_msg = message.replace(f"#{username}:Server> ", "")
                	trimed_msg = jsonpickle.decode(trimed_msg)
                	
                	if type(trimed_msg) is dict:
                		is_handled = True
                		
                		dict_cover = trimed_msg
                		
                		tracking_list = dict_cover["tracking_list"]
                		
                		mood_list = tracking_list["mood_list"]
                		anxiety_list = tracking_list["anxiety_list"]
                		depression_list = tracking_list["depression_list"]
                		energy_list = tracking_list["energy_list"]
                		
                		# Convert numbers as strings to ints
                		mood_list = list(map(int, mood_list))
                		anxiety_list = list(map(int, anxiety_list))
                		depression_list = list(map(int, depression_list))
                		energy_list = list(map(int, energy_list))
                		
                		
                		# Remove None values
                		mood_list = list(filter(None, mood_list))
                		anxiety_list = list(filter(None, anxiety_list))
                		depression_list = list(filter(None, depression_list))
                		energy_list = list(filter(None, energy_list))
                		
                		mood_chart(mood_list, anxiety_list, depression_list, energy_list)
                	
                	# Handle task trees
                	elif type(trimed_msg) is Tree:
                		print(trimed_msg)
                		is_handled = True
                	else:
                		return (trimed_msg)
                except:
                	pass
                
                # Handle server requested returns
                if message.split(' ')[1] == "return":
                
                	return (message.replace(" return",""))
                	
                	return_msg = input("Returning> ")
                	
                	server_socket.send(return_msg.encode())                
                
                else:
                	if message == f"#{username}:Server> ": 
                		pass
                	else:
                		if is_handled == True:
                			pass
                		else:
                			# If plain message
                			return (message)

            
            
            # Handle input from user
            else:
                message = (input(f"{username}> "))
                server_socket.send(message.encode())
                

    server_socket.close()   # close connection
