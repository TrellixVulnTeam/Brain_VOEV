def main(log, graph, username):
    log.info("What's the id of the task you completed?")
    id_number = input(">> ")

    graph.run(f"\
              MATCH (t: Task)-[*]-(u: User)\
              WHERE id(t) = {id_number}\
              AND u.name = '{username}'\
              SET t.completed = 'True'\
              ", id_number=id_number, username=username)


    log.info("Task completed")

    completed = graph.run(f"\
                          MATCH (t: Task)-[*]->(T)-[*]->(u)\
                          WHERE u.name = '{username}'\
                          AND T.name= 'TaskMaster'\
                          RETURN (t.completed)\
                          ", username=username).evaluate()


    if completed == 'True':

        graph.run(f"\
                  MATCH (t: Task)-[r: Task]->(T)-[*]->(u)\
                  WHERE u.name = '{username}'\
                  AND t.completed = 'True'\
                  DELETE r\
                  ")

        graph.run(f"\
                  MATCH (t: Task),\
                  (TC)-[*]->(u)\
                  WHERE NOT (t)-[*]-()\
                  AND u.name = '{username}'\
                  AND TC.name= 'TaskCompleted'\
                  AND t.completed = 'True'\
                  CREATE (t)-[l: link]->(TC)\
                  ", username=username)
