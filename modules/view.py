def main(log, graph, journal_title, username):

    log.info("Here is your Journal from Today")

    today = graph.run(f"MATCH (j: Journal), (u: User), (J: JournalMaster) where j.name = '{journal_title}' AND u.name = '{username}' AND J.name = 'JournalMaster' RETURN (j) ", journal_title=journal_title).evaluate()

    log.info(today["name"])
    log.info(today["body"])

    mood_chart(graph, log, username, journal_title)


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


def mood_chart(graph, log, username, journal_title):

    import plotext as plt
    import sys
    import os

    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)

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

    y1 = mood_list
    y2 = anxiety_list
    y3 = depression_list
    y4 = energy_list

    y1 = flatten(y1)
    y2 = flatten(y2)
    y3 = flatten(y3)
    y4 = flatten(y4)


    # Replace None with 0's and strings with ints
    y11 = []
    y21 = []
    y31 = []
    y41 = []

    for x in y1:
        if x is None:
            y11.append(0)
        if isinstance(x, str):

            try:
               x1 = [int(s) for s in x.split('"')]
            except:
                pass
            try:
                x1 = [int(s) for s in x.split(',')]
            except:
                pass

            for x2 in x1:
                y11.append(int(x2))
        if isinstance(x, int):
            y11.append(x)

    for x in y2:
        if x is None:
            y21.append(0)
        if isinstance(x, str):

            try:
                x1 = [int(s) for s in x.split('"')]
            except:
                pass
            try:
                x1 = [int(s) for s in x.split(',')]
            except:
                pass

            for x2 in x1:
                y21.append(int(x2))
        if isinstance(x, int):
            y21.append(x)

    for x in y3:
        if x is None:
            y31.append(0)
        if isinstance(x, str):

            try:
               x1 = [int(s) for s in x.split('"')]
            except:
                pass
            try:
                x1 = [int(s) for s in x.split(',')]
            except:
                pass

            for x2 in x1:
                y31.append(int(x2))
        if isinstance(x, int):
            y31.append(x)

    for x in y4:
        if x is None:
            y41.append(0)
        if isinstance(x, str):

            try:
               x1 = [int(s) for s in x.split('"')]
            except:
                pass
            try:
                x1 = [int(s) for s in x.split(',')]
            except:
                pass


            for x2 in x1:
                y41.append(int(x2))
        if isinstance(x, int):
            y41.append(x)

    x = len(y11)

    plt.plot(y11, color="yellow", label="Overall Mood")
    plt.plot(y21, color="green", label="Anxiety")
    plt.plot(y31, color="magenta", label="Depression")
    plt.plot(y41, color="blue", label="Energy")

    plt.ylim(0, 10)
    plt.yfrequency(1)
    plt.plotsize(100, 100)
    plt.xlabel("Entries")
    plt.ylabel("Mood")
    plt.title("Mood")

    plt.show()

    input(">> Press Enter to continue")
