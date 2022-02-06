from rich.tree import Tree
from rich import print


def main(log, graph):

    log.info("Here are your tasks:\n")

    tasks_in = graph.run("MATCH (n: Task) RETURN (n)")

    task_tree = Tree("Tasks")

    for task in tasks_in:

        task = task["n"]

        if task["completed"] == "False":

            task_tree.add(task["name"])

    print(task_tree)
