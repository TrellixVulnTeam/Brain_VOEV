from rich.tree import Tree
from rich import print


def main(log, graph, username):

    log.info("Subtask to attach? (id)")
    subtask = input(">> ")

    log.info("Task to attach to? (id)")
    Task = input(">> ")

    # Delete parent relationship of subtask
    graph.run(f"\
              MATCH (t: Task)-[r]->(p)\
              WHERE id(t) = {subtask}\
              DELETE r\
              ",subtask=subtask)


    # Attach node
    graph.run(f"\
              MATCH (t: Task),\
              (t2: Task),\
              (T: TaskMaster),\
              (u: User)\
              \
              WHERE id(t) = {Task}\
              AND id(t2) = {subtask}\
              AND u.name = '{username}'\
              AND T.name = 'TaskMaster'\
              AND (T)-[*]->(u)\
              \
              CREATE (t2)-[r2: Subtask_of]->(t)\
              ", Task=Task, subtask=subtask, username=username)


    # Move node up one layer
    layer = graph.run(f"\
                      MATCH (t: Task)\
                      WHERE id(t) = {subtask}\
                      RETURN t.layer\
                      ", subtask=subtask).evaluate()

    layer = int(layer) + 1

    graph.run(f"\
              MATCH (t: Task)\
              WHERE id(t)  = {subtask}\
              SET t.layer = '{layer}'\
              ", subtask=subtask, layer=layer)


if __name__ == "__main__":

    main()
