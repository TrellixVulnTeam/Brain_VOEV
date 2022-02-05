def main(log, graph):

    log.info("Here are your tasks:\n")

    tasks_in = graph.run("MATCH (n: Task) RETURN PROPERTIES (n) ")
    tasks_in = tasks_in.data()

    for x in tasks_in:
        if x['PROPERTIES (n)']["completed"] == "False":
            log.info(x['PROPERTIES (n)']["name"])
