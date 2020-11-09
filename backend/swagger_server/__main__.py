#!/usr/bin/env python3

import connexion
from swagger_server import app

application = app.app # expose global WSGI application object
if __name__ == '__main__':
    app.run(server='tornado', port=8080)
