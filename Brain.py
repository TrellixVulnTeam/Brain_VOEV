import logging
import datetime
from datetime import datetime
from py2neo import Graph
import json
import websocket
from websocket import create_connection
import threading

# Import rich

from rich.console import Console
from rich.theme import Theme
from rich.traceback import install
from rich.logging import RichHandler

# Modules

from modules import logger
from modules import view
from modules import create
from modules import update
from modules import create_task
from modules import tasks
from modules import complete_task
from modules import BrainAPI
from modules import attach


# Varibles

global user_input
user_input = "None"

global log
log = logging.getLogger("rich")


def graph_init():

    global graph
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"
    try:
        graph = Graph(uri, auth=(user, password))
    except:
        log.info("No Database Found\n")
        log.info("Start Database and press press any key to continue\n")
        input()


#  Use YYYY-MM-DD format

today = datetime.now()
date_format = today.strftime("%Y_%m_%d")
hour_min = today.strftime("%H:%S")
journal_title = f"Journal_{date_format}"


def rich_init():

    install()

    global console
    console = Console(record=True)
    custom_theme = Theme({"1": "red"})
    console = Console(theme=custom_theme)

    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    global log
    log = logging.getLogger("rich")


def switchboard():

    global log
    global graph
    global user_input
    while user_input != 'exit':

        user_input = input(">>")

        if user_input == "view":
            view.main(log, graph, journal_title)
        elif user_input == "create":
            create.main(log, graph, journal_title, date_format)
        elif user_input == "query":
            query1()
        elif user_input == "update":
            update.main(log, graph, journal_title)
        elif user_input == "tasks":
            tasks.main(log, graph)
        elif user_input == "create task":
            create_task.main(log, graph, journal_title, date_format, hour_min)
        elif user_input == "complete task":
            complete_task.main(log, graph)
        elif user_input == "attach":
            attach.main(log, graph)

    log.info("Program exiting\n")


def display_titlebar():

    global log
    log.info("""******************
*Welcome To Brain*
******************""")


if __name__ == "__main__":

    log = logging.getLogger("rich")

    try:
        rich_init()
        graph_init()
        logger.init()
        BrainAPI.main(log, json, websocket, create_connection, threading)
    except:
        log.info("Init Failed")
        console.print_exception()
    else:
        log.info("Init Succeeded!")

    display_titlebar()

    try:
        switchboard()
    except KeyboardInterrupt:
        log.info("Program exiting\n")
