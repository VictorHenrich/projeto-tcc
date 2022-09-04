from services import server

#@server.start
def start_migrate():
    from src import models

    server\
        .databases\
        .get_database()\
        .migrate()

@server.start
def start_api():
    server.websocket.run()


server.start_server()
