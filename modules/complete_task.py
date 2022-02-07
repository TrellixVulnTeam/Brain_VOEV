def main(log, graph):
    log.info("What's the id of the task you completed?")
    id_number = input(">> ")

    graph.run(f"MATCH (n: Task) WHERE id(n) = {id_number} SET n.completed = 'True' ")

    log.info(id_number)
    log.info("Task completed")
