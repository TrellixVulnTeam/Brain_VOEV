import Chatrooms
import os
import sys
import inspect


def main(log, graph, journal_title, date_format, sender_name, sender_socket, room):

    class send:
    	def __init__(self, message):
    		self.room = room
    		self.sender_name = "Server"
    		self.sender_socket = list(room.client_list.keys())[0]
    		Chatrooms.message_broadcast(self.room, self.sender_name, self.sender_socket, message)
    
    username = sender_name
    
    send("Let's create a new Journal entry")
    is_journal_created_today = graph.run(f"MATCH (j: Journal), (u: User), (J: JournalMaster) WHERE j.name = '{journal_title}' AND u.name = '{username}' AND (j)-[*]-(J)-[*]-(u) RETURN j.is_journal_created_today ", journal_title=journal_title, username=username).evaluate()


    if is_journal_created_today == 1:
        send("You have already created a journal today, here it is")

        journal_body_title, journal_body = graph.run(f"MATCH (j: Journal), (u: User), (J: JournalMaster) WHERE j.name = '{journal_title}' AND u.name = 'username' AND (j)-[*]->(J)-[*]-(u) RETURN j.name, j.body", journal_title=journal_title).evaluate()

        send(journal_body_title)
        send(journal_body)

    elif is_journal_created_today is None:

        graph.run(f"MATCH (u: User), (J: JournalMaster) WHERE u.name = '{username}' CREATE (j: Journal)-[r: Journal_of]->(J) SET j.name = '{journal_title}', j.is_journal_created_today = 1", journal_title=journal_title, username=username)
        send("Your title is " + date_format)

        # journal = multiline input
        journal =  []
        while True:
            line = input(">> ")
            if line:
                journal.append(line)
            else:
                break
        text = '\n'.join(journal)


        journal_body = ""
        for item in journal:
            journal_body+=str(item)

            send(journal_body)

        graph.run(f"MATCH (u: User), (J: JournalMaster), (j: Journal) WHERE u.name = '{username}' AND j.name = '{journal_title}' AND (j)-[*]->(J)-[*]->(u) SET j.name = '{journal_title}', j.body = '{journal_body}' ", journal_title=journal_title, journal_body=journal_body)

        # Get user input for dicts

        send("Lets add an update to your day")
        send("On a scale of 1 - 10 how is your;")

        mood = int(input(">> Overall Mood? "))
        anxiety = int(input(">> Anxitey? "))
        depression = int(input(">> Depression? "))
        energy = int(input(">> Energy? "))

        # Convert dict to string, remove brackets

        journal_body = str(journal_body)
        journal_body = journal_body.replace('[', '')
        journal_body = journal_body.replace(']', '')
        journal_body = journal_body.replace("'", '')

        anxiety = str(anxiety)
        anxiety = anxiety.replace('[', '')
        anxiety = anxiety.replace(']', '')
        anxiety = anxiety.replace("'", '')

        mood = str(mood)
        mood = mood.replace('[', '')
        mood = mood.replace(']', '')
        mood = mood.replace("'", '')

        depression = str(depression)
        depression = depression.replace('[', '')
        depression = depression.replace(']', '')
        depression = depression.replace("'", '')

        energy = str(energy)
        energy = energy.replace('[', '')
        energy = energy.replace(']', '')
        energy = energy.replace("'", '')

        # Send changes to database

        graph.run(f"MATCH (j: Journal), (J: JournalMaster), (u: User) WHERE j.name = '{journal_title}' AND u.name = '{username}' AND (j)-[*]->(J)-[*]->(u) SET j.mood = '{mood}', j.anxiety = '{anxiety}', j.depression = '{depression}', j.energy = '{energy}' ", mood=mood, journal_title=journal_title, anxiety=anxiety, depression=depression, energy=energy, username=username)
