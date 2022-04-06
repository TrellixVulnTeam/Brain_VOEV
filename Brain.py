import logging
import datetime
from datetime import datetime
from py2neo import Graph
import json
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
from modules import graph_init
from modules import login



# Varibles

global user_input
user_input = "None"

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
    return log


def switchboard(username):

    global log
    global graph
    global user_input
    while user_input != 'exit':

        user_input = input(">>")

        if user_input == "view":
            view.main(log, graph, journal_title, username)
        elif user_input == "create":
            create.main(log, graph, journal_title, date_format, username)
        elif user_input == "query":
            query1()
        elif user_input == "update":
            update.main(log, graph, journal_title, username)
        elif user_input == "tasks":
            tasks.main(log, graph, username)
        elif user_input == "create task":
            create_task.main(log, graph, journal_title, date_format, hour_min, username)
        elif user_input == "complete task":
            complete_task.main(log, graph, username)
        elif user_input == "attach":
            attach.main(log, graph, username)

    log.info("Program exiting\n")


def display_titlebar():

    global log
    log.info("""******************
*Welcome To Brain*
******************""")


if __name__ == "__main__":

    try:
        rich_init()
        graph_init()
        logger.init()
        BrainAPI.main(log, json, threading)
    except:
        log.info("Init Failed")
        console.print_exception()
    else:
        log.info("Init Succeeded!\n")

    display_titlebar()

    try:
        switchboard(username)
    except KeyboardInterrupt:
        log.info("Program exiting\n")
