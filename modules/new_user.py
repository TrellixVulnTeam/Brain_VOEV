import getpass

class user():

    def __init__(self, log, graph):

        self.privileges = "user"

        log.info("Username?")
        self.user = input(">>")

        username = self.user

        log.info("Password?")
        pass1 = getpass.getpass(">>")

        log.info("Reenter password to verify")
        pass2 = getpass.getpass(">>")

        while pass1 != pass2:
            log.info("Passwords did not match, Try again")

            log.info("Password?")
            pass1 = getpass.getpass(">>")
            log.info("Reenter password to verify")
            pass2 = getpass.getpass(">>")
        else:
            log.info("Passwords matched")

        self.password = pass2

        graph.run(f"MATCH (m: Main) CREATE (u: User), (T: TaskMaster), (J: JournalMaster) SET u.name = '{username}',  T.name = 'TaskMaster', J.name = 'JournalMaster' CREATE (u)-[r: link]->(m), (J)-[s: link]->(u), (T)-[t: link]->(u)", username=username)

        user = self.user
        password = self.password
        privileges = self.privileges

        graph.run(f"MATCH (u: User) WHERE u.name = '{user}' SET u.user = '{user}', u.password = '{password}', u.privileges = '{privileges}'", user=user, password=password, privileges=privileges)

        log.info("User created")
