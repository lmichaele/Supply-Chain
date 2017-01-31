from cherrypy import wsgiserver
#This can be from cherrypy import wsgiserver if you're not running it standalone.
import os
import django.core.handlers.wsgi

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    server = wsgiserver.CherryPyWSGIServer(
        ('0.0.0.0', 8000),
        django.core.handlers.wsgi.WSGIHandler(),
        server_name='www.django.example',
        numthreads = 20,
    )
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
