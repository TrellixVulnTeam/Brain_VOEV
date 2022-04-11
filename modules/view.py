import json
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


    today = graph.run(f"MATCH (j: Journal), (u: User), (J: JournalMaster) where j.name = '{journal_title}' AND u.name = '{username}' AND J.name = 'JournalMaster' RETURN (j) ", journal_title=journal_title).evaluate()

    journal_body = today["body"]
    
    send(f"\n Here is your journal entry for today\n Journal title: {journal_title}\n Body {journal_body}\n")
    

    mood_in =  graph.run(f"MATCH (j: Journal), (u: User), (J: JournalMaster) WHERE u.name = '{username}' AND J.name = 'JournalMaster' RETURN j.mood", journal_title=journal_title)
    anxiety_in = graph.run(f"MATCH (j: Journal), (u: User), (J: JournalMaster) WHERE u.name = '{username}' AND J.name = 'JournalMaster' RETURN (j.anxiety)", journal_title=journal_title)
    depression_in = graph.run(f"MATCH (j: Journal), (u: User), (J: JournalMaster) WHERE u.name = '{username}' AND J.name = 'JournalMaster' RETURN (j.depression)", journal_title=journal_title)
    energy_in = graph.run(f"MATCH (j: Journal), (u: User), (J: JournalMaster) WHERE u.name = '{username}' AND J.name = 'JournalMaster' RETURN (j.energy)", journal_title=journal_title)

    mood_list = []
    while mood_in.forward():
        mood_list.append(mood_in.current[0])

    anxiety_list = []
    while anxiety_in.forward():
        anxiety_list.append(anxiety_in.current[0])

    depression_list = []
    while depression_in.forward():
        depression_list.append(depression_in.current[0])

    energy_list = []
    while energy_in.forward():
        energy_list.append(energy_in.current[0])

    tracking_list = {}
    dict_cover = {}
    
    
    tracking_list["mood_list"] = mood_list
    tracking_list["anxiety_list"] = anxiety_list
    tracking_list["depression_list"] = depression_list
    tracking_list["energy_list"] = energy_list
    
    dict_cover["tracking_list"] = tracking_list
    
    dict_cover = json.dumps(dict_cover)
    send(dict_cover)
