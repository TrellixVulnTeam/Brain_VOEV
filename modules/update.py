import Chatrooms


def main(log, graph, journal_title, sender_name, sender_socket, room):

    BUFFER_SIZE = 2048
    
    username = sender_name
    
    class send:
    	def __init__(self, message):
    		self.room = room
    		self.server_name = "Server"
    		self.server_socket = list(room.client_list.keys())[0]
    		Chatrooms.message_broadcast(self.room, self.server_name, self.server_socket, message)
    
    # Get mood cursor from database

    today  =  graph.run(f"\
                        MATCH (u: User),\
                        (j: Journal),\
                        (J: JournalMaster)\
                        WHERE j.name = '{journal_title}'\
                        AND u.name = '{username}'\
                        AND (j)-[*]->(J)-[*]->(u)\
                        RETURN j\
                        ", journal_title=journal_title).evaluate()

    journal_body = today["body"]
    journal_name = today["name"]

    send("Here is your journal entry for today")
    send(journal_name + "\n")
    send(journal_body)
    
    
    send("return "+"Journal body?")
    journal_body = sender_socket.recv(BUFFER_SIZE).decode()
    

    #

    mood = []
    anxiety = []
    depression = []
    energy = []

    mood.append(today["mood"])
    anxiety.append(today["anxiety"])
    depression.append(today["depression"])
    energy.append(today["energy"])

    # Flatten list of lists

    mood = flatten(mood)
    anxiety = flatten(anxiety)
    depression = flatten(depression)
    energy = flatten(energy)

    # Get user input
    
    send("Lets add an update to your day")
    send("On a scale of 1 - 10 how is your;")
        
    send("return "+"Mood?")
    mood = sender_socket.recv(BUFFER_SIZE).decode()
        
    send("return "+"Anxiety?")
    anxiety = sender_socket.recv(BUFFER_SIZE).decode()
        
    send("return "+"Depression?")
    depression = sender_socket.recv(BUFFER_SIZE).decode()
        
    send("return " + "Energy")
    energy = sender_socket.recv(BUFFER_SIZE).decode()
    
    send(f"\n Body: {journal_body} Mood: {mood} Anxiety: {anxiety} Depression: {depression} Energy: {energy}")
    

    # Convert dict to string, remove brackets

    journal_body = str(journal_body)
    journal_body = journal_body.replace('[', '')
    journal_body = journal_body.replace(']', '')
    journal_body = journal_body.replace("'", '')

    anxiety = str(anxiety)
    anxiety = anxiety.replace('[','')
    anxiety = anxiety.replace(']','')
    anxiety = anxiety.replace("'",'')

    mood = str(mood)
    mood = mood.replace('[','')
    mood = mood.replace(']','')
    mood = mood.replace("'",'')

    depression = str(depression)
    depression = depression.replace('[','')
    depression = depression.replace(']','')
    depression = depression.replace("'",'')

    energy = str(energy)
    energy = energy.replace('[','')
    energy = energy.replace(']','')
    energy = energy.replace("'",'')

    # Update database with node

    graph.run(f"\
              MATCH (u: User),\
              (j: Journal)\
              WHERE j.name = '{journal_title}'\
              SET j.body = '{journal_body}',\
              j.mood = '{mood}',\
              j.anxiety = '{anxiety}',\
              j.depression = '{depression}',\
              j.energy = '{energy}'\
              ", journal_title=journal_title,  journal_body=journal_body, mood=mood, anxiety=anxiety, depression=depression, energy=energy)


def flatten(t):

    flat_list = []
    # Iterate through the outer list
    for element in t:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list
