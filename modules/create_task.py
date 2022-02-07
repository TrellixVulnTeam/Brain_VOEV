def main(log, graph, journal_title, date_format, hour_min):

    taskname_in = input(">> Task name? ")
    task_datetime = (f"Task {date_format} {hour_min} {taskname_in}")

    taskname = taskname_in

    completed = False

    graph.run(f"CREATE (n: Task) SET n.name = '{taskname}' SET n.task_datetime = '{task_datetime}' SET n.completed = '{completed}' ", task_datetime=task_datetime, taskname=taskname)

    id_number = graph.run(f"MATCH (n: Task) WHERE n.name = '{taskname}' RETURN ID (n)", taskname=taskname).evaluate()

    name2 = f"{taskname} (id: {id_number})"

    graph.run(f"MATCH (n: Task) WHERE n.name = '{taskname}' SET n.name = '{name2}'", taskname=taskname, id_number=id_number)
    graph.run(f"MATCH (a: Task), (b: Task_master) WHERE a.name = '{name2}' AND b.name = 'Task_master' CREATE (a)-[r: Task]->(b)", name2=name2)

    log.info(name2)
    log.info("Task created")
