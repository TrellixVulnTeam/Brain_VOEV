import os
from py2neo import Graph
import time
import logging

from modules import new_user


def connect(log):

    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = os.getenv('BrainDBPassword')
    try:
        graph = Graph(uri, auth=(user, password))
    except:
        log.info("No Database Found\n")
        log.info("Start Database and press press any key to continue\n")
        input()
    
    return graph

def create_system(log, graph):
    graph.run(f"CREATE (n: Main) SET n.name = 'Main'")

    log.info("You must create a user profile to continue")

    user = new_user.user(log, graph)
    
    username = user.name

    log.info(username)

    graph.run(f"MATCH (m: Main) CREATE (a: user), (b: TaskMaster), (c: JournalMaster) SET a.name = '{username}',  b.name = 'TaskMaster', c.name = 'JournalMaster' CREATE (b)-[r: link]->(a), (c)-[s: link]->(a), (a)-[t: link]->(m)", username=username)

    return user


def system_init(log, graph):

    main = graph.run(f"MATCH (n: Main) WHERE n.name='Main' RETURN (n)").evaluate()
    time.sleep(1)
    
    if main == None:
        log.info("No data found. Initializing system.")
        user = create_system(log, graph)
        return user
    else:
        pass

def main(log):
    graph = connect(log)
    user = system_init(log, graph)
    return user, graph
