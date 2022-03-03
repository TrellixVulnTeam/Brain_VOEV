from rich.tree import Tree
from rich import print


def main(log, graph):

    log.info("Here are your tasks:\n")

    tasks_in = graph.run("MATCH (n: Task) RETURN n").data()

    task_tree = Tree("Tasks")

    task_branch_names = {}
    task_branch_names["Task_master_Branch"] = task_tree

    for task in tasks_in:

        task = task["n"]
        taskname = task["name"]

        relationship = graph.run(f"MATCH (a: Task)-[r]->(b) WHERE a.name = '{taskname}' RETURN type(r)", taskname=taskname).data()

        if relationship != []:
            relationship = relationship[0]["type(r)"]
        else:
            relationship = "Task_of"

        parent = graph.run(f"MATCH (a: Task)-[r]->(b) WHERE a.name = '{taskname}' RETURN b", taskname=taskname).data()
        if parent != []:
            parent = parent[0]["b"]["name"]
        else:
            parent = "Task_master" + "_Branch"

        task_branch_name = taskname + "_Branch"

        if parent != None:
            parent_branch_name = parent + "_Branch"
        else:
            parent_branch_name = "Task_master" + "_Branch"

        if task["completed"] == "False":

                if parent_branch_name not in task_branch_names:
                    task_branch_names[parent_branch_name] = parent_branch_name

                    grandparent = graph.run(f"MATCH (a)-[r]->(b)-[r2]->(c) WHERE a.name = '{taskname}' RETURN c", taskname=taskname).data()

                    if grandparent != []:
                        print(grandparent)
                        grandparent = grandparent[0]["c"]["name"]
                        grandparent_branch_name = grandparent + "_Branch"
                    else:
                        grandparent_branch_name = "Task_master" + "_Branch"

                    task_branch_names[parent_branch_name] = task_branch_names[grandparent_branch_name].add(parent)

                if task_branch_name not in task_branch_names:
                    task_branch_names[task_branch_name] = task_branch_names[parent_branch_name].add(taskname)

    print(task_tree)
