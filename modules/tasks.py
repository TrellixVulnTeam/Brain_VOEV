from rich.tree import Tree
from rich import print


def main(log, graph, username):

    log.info("Here are your tasks:\n")

    tasks_in = graph.run(f"MATCH (t: Task), (u: User), (T: TaskMaster) WHERE u.name = '{username}' AND T.name = 'TaskMaster' AND (t)-[*]->(T)-[*]->(u) RETURN t", username=username).data()

    task_tree = Tree("Tasks")

    task_branch_names = {}
    task_branch_names["Task_master_Branch"] = task_tree

    for task in tasks_in:

        task = task["t"]
        taskname = task["name"]

        relationship = graph.run(f"MATCH (t: Task)-[r]->(T)-[*]->(u), (u: User), (T: TaskMaster) WHERE u.name = '{username}' AND T.name = 'TaskMaster' AND t.name = '{taskname}' RETURN type(r)", taskname=taskname, username=username).data()
        
        relationship = relationship[0]["type(r)"]

        parent = graph.run(f"MATCH (t: Task)-[r]->(T)-[*]->(u), (u: User), (T: TaskMaster) WHERE u.name = '{username}' AND T.name = 'TaskMaster' AND t.name = '{taskname}' RETURN t", taskname=taskname, username=username).data()
        
        parent = parent[0]["t"]["name"]

        task_branch_name = taskname + "_Branch"

        parent_branch_name = parent + "_Branch"

        if task["completed"] == "False":

                if parent_branch_name not in task_branch_names:
                    task_branch_names[parent_branch_name] = parent_branch_name

                    grandparent = graph.run(f"MATCH (t)-[r]->(b)-[r2]->(c)-[*]->(T)-[*]->(u) WHERE t.name = '{taskname}' AND T.name = 'TaskMaster' AND u.name = '{username}' RETURN c", taskname=taskname, username=username).data()

                    grandparent = grandparent[0]["c"]["name"]
                    grandparent_branch_name = grandparent + "_Branch"

                    task_branch_names[parent_branch_name] = task_branch_names[grandparent_branch_name].add(parent)

                if task_branch_name not in task_branch_names:
                    task_branch_names[task_branch_name] = task_branch_names[parent_branch_name].add(taskname)

    print(task_tree)
