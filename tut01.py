import cherrypy

cherrypy.config.update(
    {'server.socket_host': '0.0.0.0'} )      
cherrypy.engine.start()


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"


if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
