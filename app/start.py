from services import server

#@server.start
def start_migrate():
    from src import models

    server\
        .databases\
        .get_database()\
        .migrate()

#@server.start
def start_api():
    from src import routes

    server.api.run()

#@server.start
def start_websocket():
    from src.controllers import ws

    server.websocket.run()


server.start_server()
