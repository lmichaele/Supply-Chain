import cherrypy
import os, os.path

localDir = os.path.abspath(os.path.dirname(__file__))
CA = os.path.join(localDir, 'server.crt')
KEY = os.path.join(localDir, 'server.key')
def setup_server():

    class Root:
        @cherrypy.expose

    def index(self):
       return "Hello there!"
	
cherrypy.tree.mount(Root())
if __name__ == '__main__':

setup_server()
cherrypy.config.update({'server.socket_port': 8443,
   'environment': 'production',
   'log.screen': True,
   'server.ssl_certificate': CA,
   'server.ssl_private_key': KEY})
	
cherrypy.server.quickstart()
cherrypy.engine.start()
