import os
import cherrypy
import uuid
import utils


class StringGenerator(object):    
    @cherrypy.expose
    def index(self):
        return "Тестовый сервер API v1"

    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def test_list(self):
        tests = os.listdir(path='./tests')
        tests = {i : tests[i] for i in range(len(tests))}
        return tests
                
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_uuid(self, test="", name="", num="", letter=""):
        new_uuid = str(uuid.uuid4())
        print(new_uuid, test, name, num, letter)
        return utils.tbl_new_uuid(new_uuid, test, name, num, letter)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_test(self, UUID="", task=""):
        print(UUID, task)
        return utils.tbl_get_test(UUID, task)
        
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_full_test_and_lock(self, UUID=""):
        print(UUID)
        return utils.tbl_get_full_test_and_lock(UUID)
        
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def set_answ(self, UUID="", task="", answ=""):
        print(UUID, task, answ)
        return utils.tbl_set_answ(UUID, task, answ)


if __name__ == '__main__':
    conf = {
        'global': {
            'server.socket_port': 9090,
        },
        '/': {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Access-Control-Allow-Origin', '*')],
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
    }
    cherrypy.quickstart(StringGenerator(), '/', conf)
