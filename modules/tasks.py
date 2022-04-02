from rich.tree import Tree
from rich import print


def main(log, graph, username):

    log.info("Here are your tasks:\n")

    tasks_in = graph.run(f"MATCH (t: Task), (u: User), (T: TaskMaster) WHERE u.name = '{username}' AND T.name = 'TaskMaster' AND (t)-[*]->(T)-[*]->(u) RETURN t", username=username).data()


    task_tree = Tree("Tasks")
    task_list = {}

    for task in tasks_in:

        task = task["t"]
        taskname = task["name"]


        if task["completed"] == "False":

            parent = graph.run(f"MATCH (t: Task)-[*]->(p: Task) WHERE t.name = '{taskname}' RETURN (p)", taskname=taskname).evaluate()


            if parent and (parent != "TaskMaster") and (parent != "") and (parent != username) and (parent != None):

                parent = parent["name"]

                if parent not in task_list.values():
                    task_list[taskname] = parent

                    parent_tree = task_tree.add(parent)
                    parent_tree.add(taskname)
            else:
                parent is None


            if parent:
                if taskname not in task_list.keys():
                    log.info(taskname)
                    log.info(str(parent_tree))

                    task_list[taskname] = parent
                    taskname_tree = parent_tree.add(taskname)
            elif parent == None:
                if taskname not in task_list.keys():
                    task_list[taskname] = parent
                    taskname_tree = task_tree.add(taskname)

    log.info(task_list)
    print(task_tree)
