from typing import Callable

import flask

from mat_server.app.mat_server.routes_ext import RoutesExt


class MatServer:

    def __init__(self,
                 flask_app: flask.Flask,
                 routes_ext: RoutesExt,
                 wsgi_application_prod_serve_func: Callable):
        self._flask_app = flask_app

        self._routes_ext = routes_ext
        self._routes_ext.init_app(self._flask_app)

        self._wsgi_application_prod_serve_func = wsgi_application_prod_serve_func

    def get_app(self):
        return self._flask_app

    def serve(self, host: str, port: int):
        self._wsgi_application_prod_serve_func(self._flask_app, host=host, port=port)
