import os
import cherrypy
import uuid
import utils
# from cherrypy.lib import static


class StringGenerator:    
    @cherrypy.expose
    def index(self):
        return "Тестовый сервер API v1"

    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def test_list(self):
        tests = os.listdir(path='./tests')
        tests = [test for test in tests if test[0] != "_"]
        tests.sort()
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

      
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_db(self, KEY=""):
        with open('./KEY.txt') as key_f:
            PASS=key_f.readline().rstrip()
            print(f'get_db {PASS} : {KEY}')      
        if KEY == PASS:
            return utils.tbl_get_db()
        return "Error: The KEY parameter is incorrect"
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def backup_db(self, KEY=""):
        with open('./KEY.txt') as key_f:
            PASS=key_f.readline().rstrip()
            print(f'get_db {PASS} : {KEY}')      
        if KEY == PASS:
            return utils.tbl_backup()
        return "Error: The KEY parameter is incorrect"


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_headers(self, KEY=""):
        with open('./KEY.txt') as key_f:
            PASS=key_f.readline().rstrip()
            print(f'get_headers {PASS} : {KEY}')      
        if KEY == PASS:
            return utils.tbl_get_headers()
        return "Error: The KEY parameter is incorrect"


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_results(self, KEY="", TIME_START="", NUM="", LETTER="", TEST=""):
        with open('./KEY.txt') as key_f:
            PASS=key_f.readline().rstrip()
            print(f'get_results {PASS} : {KEY}')      
        if KEY == PASS:
            return utils.tbl_get_results(TIME_START, NUM, LETTER, TEST)
        return "Error: The KEY parameter is incorrect"



    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_test_py(self, KEY="", TEST=""):
        with open('./KEY.txt') as key_f:
            PASS=key_f.readline().rstrip()
            print(f'get_results {PASS} : {KEY}')      
        if KEY == PASS:
            return utils.get_test_py(TEST)
        return "Error: The KEY parameter is incorrect"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def save_test_py(self, KEY="", TEST="", CODE=""):
        with open('./KEY.txt') as key_f:
            PASS=key_f.readline().rstrip()
            print(f'get_results {PASS} : {KEY}')      
        if KEY == PASS:
            return utils.save_test_py(TEST, CODE)
        return "Error: The KEY parameter is incorrect"


'''
    @cherrypy.expose
    def get_40_tests(self, KEY="", TEST=""):
        with open('./KEY.txt') as key_f:
            PASS=key_f.readline().rstrip()
            print(f'get_40_tests {PASS} : {KEY}')      
        if KEY == PASS:
            return static.serve_fileobj(utils.get_40_tests(TEST), 'application/x-download', 'attachment', 'test.docx')
        return "Error: The KEY parameter is incorrect"
'''

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
