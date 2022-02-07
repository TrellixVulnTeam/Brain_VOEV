from rich.tree import Tree
from rich import print


def main(log, graph):

    log.info("Here are your tasks:\n")

    tasks_in = graph.run("MATCH (n: Task) RETURN n").data("n")

    task_tree = Tree("Tasks")

    task_branch_names = {}

    for task in tasks_in:

        task = task["n"]
        taskname = task["name"]

        relationship = graph.run(f"MATCH (n: Task)-[r]->() WHERE n.name = '{taskname}' RETURN type(r)", taskname=taskname).data()
        relationship = relationship[0]["type(r)"]

        if relationship == "Task":
            parent = graph.run("MATCH (a: Task)-[r: Task]->(b: Task) RETURN b").data()
        elif relationship == "Subtask_of":
            parent = graph.run("MATCH (a: Task)-[r: Subtask_of]-(b: Task) RETURN b").data()
            parent = parent[0]["b"]["name"]

        if task["completed"] == "False":

            task_branch_name = taskname + "_Branch"

            if relationship == "Task":

                if task_branch_name in task_branch_names:
                    pass
                elif task_branch_name not in task_branch_names:
                    task_branch_names[task_branch_name] = task_tree.add(taskname)

            elif relationship == "Subtask_of":

                parent_branch_name = parent + "_Branch"

                if parent_branch_name in task_branch_names:

                    if task_branch_name in task_branch_names:
                        pass
                    elif task_branch_name not in task_branch_names:
                        task_branch_names[task_branch_name] = task_branch_names[parent_branch_name].add(taskname)

                elif parent_branch_name not in task_branch_names:

                    task_branch_names[parent_branch_name] = task_tree.add(parent)
                    if task_branch_name in task_branch_names:
                        pass
                    elif task_branch_name not in task_branch_names:
                        task_branch_names[task_branch_name] = task_branch_names[parent_branch_name].add(taskname)

    print(task_tree)
