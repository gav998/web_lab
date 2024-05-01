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
        """
        Возвращает список доступных тестов.

        Returns:
            dict: Словарь, где ключами являются индексы тестов, а значениями - названия тестов.
        """
        tests = os.listdir(path='./tests')
        tests = [test for test in tests if test[0] != "_"]
        tests.sort()
        tests = {i : tests[i] for i in range(len(tests))}
        return tests
                
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_uuid(self, test="", name="", num="", letter=""):
        """
        Генерирует уникальный идентификатор и тест. Добавляет запись в БД.

        Args:
            test (str): Параметр теста.
            name (str): Параметр имени.
            num (str): Параметр номера.
            letter (str): Параметр буквы.

        Returns:
            dict: Уникальный идентификатор теста
        """
        new_uuid = str(uuid.uuid4())
        print(new_uuid, test, name, num, letter)
        return utils.tbl_new_uuid(new_uuid, test, name, num, letter)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def test_1(self, oil="", dollar=""):
        """
        test_1
        """
        
        return {"desc": "Hello, World",
                "ertyuiuyt": str(int(oil)*int(dollar))
                }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_test(self, UUID="", task=""):
        """
        Получает тест по указанному UUID и заданию.

        Args:
            UUID (str): Уникальный идентификатор теста. По умолчанию пустая строка.
            task (str): Номер задания теста. По умолчанию пустая строка.

        Returns:
            dict: Одно задание теста.
        """
        print(UUID, task)
        return utils.tbl_get_test(UUID, task)
        
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_full_test_and_lock(self, UUID=""):
        """
        Устанавливает бит блокировки и получает полный тест по указанному UUID.

        Args:
            UUID (str): Уникальный идентификатор теста. По умолчанию пустая строка.

        Returns:
            dict: Строка записи в БД
        """
        print(UUID)
        return utils.tbl_get_full_test_and_lock(UUID)
        
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def set_answ(self, UUID="", task="", answ=""):
        """
        Устанавливает ответ для указанного задания в тесте.

        Args:
            UUID (str): Уникальный идентификатор теста. По умолчанию пустая строка.
            task (str): Уникальный идентификатор задания. По умолчанию пустая строка.
            answ (str): Ответ на задание. По умолчанию пустая строка.

        Returns:
            dict: ANSW_TIME
        """
        print(UUID, task, answ)
        return utils.tbl_set_answ(UUID, task, answ)

    @cherrypy.expose
    def test_upload(self):
        return """
        <html><body>
       
            <h2>Загрузить файл</h2>

            <form onsubmit="return false;">
            <input type="file" name="answFile" value="Выберите файл"/><br />
            <input type="submit" value="Загрузить"/>
            </form>
        <!-- JavaScript to set the values of hidden fields -->
        <script>

            document.getElementById('ANSW').type="file"
            document.getElementById('ANSW_BTN').onClick="answFile();"




            var UUID = "123asd-123asd-123asd";
            var task = 10;

function submitForm() {
    // Get the file input element
    let answFile = document.getElementById("answFile").files[0];

    let answFile = fileInput.files[0];

			upload_file(UUID, task, answFile).then(
				response => {
					console.log(response);
				},
				error => alert(`Rejected: ${error}`)
			);

    }



async function upload_file(UUID, task, answFile) {
	let url = new URL(server + "upload_file/");
	
	// Create a FormData object to send the file
    let formData = new FormData();
    formData.append('UUID', UUID);
    formData.append('task', task);
    formData.append('answ', answFile);

	let response = await fetch(url, {
            method: 'POST',
            body: formData,
        });
	if (response.ok) { // если HTTP-статус в диапазоне 200-299
		// получаем тело ответа
		let json = await response.json();
		console.log(decodeURI(url.href), '\n', json);
		return json;
	} else {
		console.log(url.href, '\n', decodeURI(url.href), '\n', "Ошибка HTTP: " + response.status);
		alert("Ошибка HTTP: " + response.status);
	}
}

        </script>


            <h2>Download a file</h2>
            <a id="href_download" href='download'>This one</a>
        </body></html>
        """


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def upload_file(self, UUID="", task="", answ=""):
        """
        Загружает файл ученика на сервер.       
        """
        print(UUID, task, answ)
        myFile = answ
        return utils.tbl_upload_file(UUID, task, myFile)


    # @cherrypy.expose
    # def download_file(self, filename="", T1="", T2="", ):
    #     if T1=="user":
    #         file_path = _USER_PATH+filename
    #     elif T2=="static":
    #         pass
    #     elif T2=="dinamic":
    #         pass
    #     else:
    #         return {"error":"T2 static or dinamic"}
        

    #     path = os.path.join(absDir, 'pdf_file.pdf')
    #     return cherrypy.lib.static.serve_file(path, 'application/x-download',
    #                              'attachment', os.path.basename(path))

      
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_db(self, KEY=""):
        """
        Возвращает базу данных, если указанный ключ совпадает с корректным ключом.

        Args:
            KEY (str): Ключ для доступа к базе данных. По умолчанию пустая строка.

        Returns:
            dict: База данных, если ключ совпадает, иначе сообщение об ошибке.
        """
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
            'server.socket_host': '0.0.0.0',
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
