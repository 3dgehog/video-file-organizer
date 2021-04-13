import cherrypy
import threading
import logging

from video_file_organizer.webserver.app import app

logger = logging.getLogger('vfo.server')


class WebServer(threading.Thread):
    def __init__(self, bind='0.0.0.0', port=5055, base_url=''):
        # String to remove unicode warning from cherrypy startup
        threading.Thread.__init__(self, name='web_server')
        self.bind = str(bind)
        self.port = port
        self.base_url = base_url

    def start(self):
        """ If we have already started and stopped a thread, we need to
        reinitialize it to create a new one"""
        if not self.is_alive():
            self.__init__(
                bind=self.bind,
                port=self.port,
                # ssl_certificate=self.ssl_certificate,
                # ssl_private_key=self.ssl_private_key,
                base_url=self.base_url,
            )
        threading.Thread.start(self)

    def _start_server(self):
        # Mount the WSGI callable object (app) on the root directory
        cherrypy.tree.graft(app, "/")

        # Unsubscribe the default server
        cherrypy.server.unsubscribe()

        # Instantiate a new server object
        server = cherrypy._cpserver.Server()

        # Configure the server object
        server.socket_host = self.bind
        server.socket_port = self.port
        server.thread_pool = 30

        server.subscribe()

        # Start the CherryPy WSGI web server
        cherrypy.engine.start()
        cherrypy.engine.block()

    def run(self):
        self._start_server()

    def stop(self):
        logger.info('Shutting down web server')
        cherrypy.engine.exit()
