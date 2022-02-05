def main(log, graph, journal_title, date_format):

    log.info("Let's create a new Journal entry")

    is_journal_created_today = graph.run("MATCH (n {name: $journal_title}) RETURN n.is_journal_created_today", journal_title=journal_title).evaluate()


    if is_journal_created_today == 1:
        log.info("You have already created a journal today, here it is")

        journal_body_title = graph.run("MATCH (n {name: $journal_title}) RETURN (n.name)", journal_title=journal_title).evaluate()

        journal_body = graph.run("MATCH (n {name: $journal_title}) RETURN (n.body)", journal_title=journal_title).evaluate()

        log.info(journal_body_title)
        log.info(journal_body)

    elif is_journal_created_today is None:

        graph.run("CREATE (n: Journal {name: $journal_title}) SET n.is_journal_created_today = 1", journal_title=journal_title)
        log.info("Your title is " + date_format)

        #journal = multiline input
        journal =  []
        while True:
            line = input(">> ")
            if line:
                journal.append(line)
            else:
                break
        text = '\n'.join(journal)

        journal_body = journal

        graph.run("MATCH (n: Journal {name: $journal_title}) SET n.name = $journal_title ", journal_title=journal_title)
        graph.run("MATCH (n: Journal {name: $journal_title}) SET n.body = $journal_body ", journal_title=journal_title, journal_body=journal_body)

        # Get user input for dicts

        log.info("Lets add an update to your day")
        log.info("On a scale of 1 - 10 how is your;")

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

        graph.run(f"MATCH (a: Journal) where a.name = '{journal_title}' SET a.mood = '{mood}'", mood=mood, journal_title=journal_title)
        graph.run(f"MATCH (a: Journal) where a.name = '{journal_title}' SET a.anxiety = '{anxiety}'", anxiety=anxiety, journal_title=journal_title)
        graph.run(f"MATCH (a: Journal) where a.name = '{journal_title}' SET a.depression = '{depression}'", depression=depression, journal_title=journal_title)
        graph.run(f"MATCH (a: Journal) where a.name = '{journal_title}' SET a.energy = '{energy}'", energy=energy, journal_title=journal_title)
        graph.run(f"MATCH (a: Journal), (b: Journal_master) WHERE a.name = '{journal_title}' CREATE (a)-[r: Journal]->(b)")
