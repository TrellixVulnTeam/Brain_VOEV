from rich.tree import Tree
from rich import print

import Chatrooms


def main(log, graph, sender_name, sender_socket, room):

    
    class send:
    	def __init__(self, message):
    		self.room = room
    		self.server_name = "Server"
    		self.server_socket = list(room.client_list.keys())[0]
    		Chatrooms.message_broadcast(self.room, self.server_name, self.server_socket, message)
    
    username = sender_name
    
    BUFFER_SIZE = 2048
    
    send("return " + "Subtask to attach? (id)")
    
    subtask = sender_socket.recv(BUFFER_SIZE).decode()

    send("return " + "Task to attach to? (id)")
    Task = sender_socket.recv(BUFFER_SIZE).decode()

    try:
        graph.run(f"MATCH (a: Task), (b: Task) WHERE id(a) = {Task} AND id(b) = {subtask} CREATE (b)-[r: Subtask_of]->(a)")
    except Exception as e:
        send(e)

    try:
        graph.run(f"MATCH (a: Task)-[r: Task]-(b: Task_master) WHERE id(a) = {subtask} AND b.name = 'Task_master' DELETE r", subtask=subtask)
    except Exception as e:
        send(e)


if __name__ == "__main__":

    main()
