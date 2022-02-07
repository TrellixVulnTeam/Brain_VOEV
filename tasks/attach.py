from rich.tree import Tree
from rich import print


def main(log, graph):

    log.info("Subtask to attach? (id)")
    subtask = input(">> ")

    log.info("Task to attach to? (id)")
    Task = input(">> ")

    try:
        graph.run(f"MATCH (a: Task), (b: Task) WHERE id(a) = {Task} AND id(b) = {subtask} CREATE (b)-[r: Subtask_of]->(a)")
    except Exception as e:
        log.info(e)

if __name__ == "__main__":

    main()
