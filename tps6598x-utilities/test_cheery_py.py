import cherrypy
import os

file_path = os.getcwd().replace("\\", "/")

class Root(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"


if __name__ == '__namin__':

    port = 1313  # enzo add
    print(port)
    cherrypy.config.update({'server.socket_host': '127.0.0.1',
                            'server.socket_port': port, })

    conf = {'/html': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': '%s/html' % file_path},
            '/css': {'tools.staticdir.on': True,
                     'tools.staticdir.dir': '%s/css' % file_path},
            '/resources': {'tools.staticdir.on': True,
                           'tools.staticdir.dir': '%s/resources' % file_path},
            '/docs': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': '%s/docs' % file_path}}

    cherrypy.quickstart(Root(), '/', config=conf)
