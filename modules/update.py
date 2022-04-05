def main(log, graph, journal_title, username):

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

    log.info("Here is your journal entry for today")
    log.info(journal_name)
    log.info(journal_body)

    # Journal = multiline input

    journal2 = []

    journal = today["body"]
    journal2.append(journal)
    while True:
        line = input(">>> ")
        if line:
            journal2.append(line)
        else:
            break
    text = '\n'.join(journal)

    journal_body = journal2
    log.info(journal_body)

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

    mood.append(int(input(">> Overall Mood? ")))
    anxiety.append(int(input(">> Anxitey? ")))
    depression.append(int(input(">> Depression? ")))
    energy.append(int(input(">> Energy? ")))

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
