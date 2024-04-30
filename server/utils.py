# Встроенные модули
from collections import Counter
import datetime
import json
import os
import subprocess
from sys import platform
import sqlite3

# Сторонние модули
import base64
from PIL import Image
from io import BytesIO

import urllib.parse as urllp


_CURR_PATH = os.path.abspath(os.getcwd())
_DB_PATH = _CURR_PATH + "/data.db"
_TEST_PATH = _CURR_PATH + "/tests/"
_USER_PATH = _CURR_PATH + "/user_files/"

def encodeURI(s): return urllp.quote(s, safe="~@#$&()*!+=:;,.?/'")
def decodeURI(s): return urllp.unquote(s, errors="strict")
def encodeURIComponent(s): return urllp.quote(s, safe="~()*!.'")
def decodeURIComponent(s): return urllp.unquote(s, errors="strict")

def image_to_base64(image_path):
    base64_str = ''  # Переменная для хранения строки в формате Base64

    try:
        with Image.open(image_path) as img:  # Открываем изображение
            buffer = BytesIO()  # Создаем буфер для сохранения изображения
            img_format = img.format  # Получаем формат изображения
            img.save(buffer, format=img_format)  # Сохраняем изображение в буфере
            img_data = buffer.getvalue()  # Получаем данные из буфера

        base64_str = base64.b64encode(img_data).decode('utf-8')  # Преобразуем данные в формат Base64 и декодируем в строку
    except Exception as e:  # В случае возникновения ошибки
        print(e)  # Выводим сообщение об ошибке
        base64_str = str(e)  # Преобразуем ошибку в строку

    return base64_str  # Возвращаем строку в формате Base64



 
def tbl_new_uuid(UUID, TEST, NAME, NUM, LETTER):
    # Генерация теста
    test = generate_test(TEST)
    if not test:
        return "Error: TEST.py not found"
    
    # Формирование строки ключей для SQL-запроса
    keys = ', '.join([f'"{key}"' for key in test.keys()])
    # Формирование строки заполнителей для SQL-запроса
    placeholders = ', '.join(['?' for _ in test.keys()])
    
    # Формирование SQL-запроса
    sql = f'''
    INSERT 
      INTO tests(UUID, TEST, NAME, NUM, LETTER, TIME_START, {keys}) 
    VALUES (?, ?, ?, ?, ?, ?, {placeholders});    
    '''
    
    # Формирование списка значений для выполнения SQL-запроса
    NAME = NAME.upper()
    values = [UUID, TEST, NAME, NUM, LETTER, datetime.datetime.today()]  
    values.extend(test.values())
    values = tuple(values)
    
    try:
        # Установление соединения с базой данных
        with sqlite3.connect(_DB_PATH) as db:
            # Выполнение SQL-запроса
            db.execute(sql, values)
            # Сохранение изменений в базе данных
            db.commit()
    except sqlite3.Error as e:
        # Обработка и вывод ошибки выполнения SQL-запроса
        print(f"Error executing SQL query: {e}")
        return {"UUID": f"Error executing SQL query: {e}"}
    finally:
        # Закрытие соединения с базой данных
        db.close()
        
    return {"UUID": UUID}

        
def tbl_get_test(UUID, TASK):
    sql = '''
    SELECT * FROM tests WHERE UUID = (?);
    '''
    
    values = tuple([UUID])
    
    try:   
        with sqlite3.connect(_DB_PATH) as db:
            column = db.execute(sql, values)
            column_names = [desc[0] for desc in column.description]
            column = column.fetchone()
            if not column:
                return {"TASK_TEXT": "Error: UUID not found"}
            test = dict(zip(column_names, column))
    except sqlite3.Error as e:
        print(f"Error executing SQL query: {e}")
        return {"TASK_TEXT": f"Error executing SQL query: {e}"}
    finally:
        db.close() 
        
    try:
        if not (1 <= int(TASK) <= test["COUNT"]):
            return {"TASK_TEXT": "Error: TASK not found"}
        pic = image_to_base64(test["T_"+TASK+"_PIC"]) if test["T_"+TASK+"_PIC"] is not None else None
        return {
                        "UUID": test["UUID"],
                        "TEST": test["TEST"],
                        "NAME": test["NAME"],
                        "NUM": test["NUM"],
                        "LETTER": test["LETTER"],
                        "TIME_START": test["TIME_START"],
                        "COUNT": test["COUNT"],
                        "LOCK": test["LOCK"],
                        
                        "TASK_TEXT": test["T_"+TASK+"_TEXT"],
                        "TASK_PIC": pic,
                        "ANSW": test["T_"+TASK+"_ANSW"],
                        "ANSW_TIME": test["T_"+TASK+"_ANSW_TIME"],
                        
                    }
    except Exception as e:
        print(f"Error: {e}")
        return {"TASK_TEXT": f"Error executing: {e}"}

"""
# на raspberry не поддерживается RETURNING в sqlite
def tbl_get_full_test_and_lock(UUID):
    sql = f'''
    UPDATE tests 
       SET 
        LOCK = 1
     WHERE UUID = (?)
     RETURNING *;
    '''
    with sqlite3.connect(DB_PATH) as db:
        column = db.execute(sql, (UUID,))
        column_names = [desc[0] for desc in column.description]
        column = column.fetchone()
        test = dict(zip(column_names, column))
        return test
"""
def tbl_get_full_test_and_lock(UUID):
    sql1 = f'''
    UPDATE tests 
       SET 
        LOCK = 1
     WHERE UUID = (?);
    '''
    sql2 = f'''SELECT * FROM tests WHERE UUID = (?);'''
    try:
        with sqlite3.connect(_DB_PATH) as db:
            db.execute(sql1, (UUID,)).fetchone()
            column = db.execute(sql2, (UUID,))
            column_names = [desc[0] for desc in column.description]
            column = column.fetchone()
            if not column:
                return {"TASK_TEXT": "Error: UUID not found"}
            #
            test = dict(zip(column_names, column))
            
            for TASK in range(1,test["COUNT"]+1):
                pic = image_to_base64(test[f"T_{TASK}_PIC"]) if test[f"T_{TASK}_PIC"] is not None else None
                test[f"T_{TASK}_PIC"] = pic
        return test
    except sqlite3.Error as e:
        print(f"Error executing SQL query: {e}")
        return {"TASK_TEXT": f"Error executing SQL query: {e}"}
    finally:
        db.close()

     
def tbl_set_answ(UUID, task, answ):
    if task.isdigit():
        task = int(task)
    else:
        task = 1
    sql = f'''
    UPDATE tests 
       SET 
        T_{task}_ANSW = (?),
        T_{task}_ANSW_TIME = (?)
     WHERE UUID = (?) and LOCK = 0;
    '''
    try:
        with sqlite3.connect(_DB_PATH) as db:
            answ_time = datetime.datetime.today()
            db.execute(sql, (answ, answ_time, UUID,))
        return {
                        "ANSW_TIME": str(answ_time),
                    }
    except sqlite3.Error as e:
        print(f"Error executing SQL query: {e}")
        return {"TASK_TEXT": f"Error executing SQL query: {e}"}
    finally:
        db.close()

    
def tbl_upload_file(UUID, task, myFile):
    if task.isdigit():
        task = int(task)
    else:
        task = 1
    
    if ("/" in UUID or
        "\\" in UUID or
        "." in UUID or
        ";" in UUID or
        "'" in UUID or 
        '"' in UUID):
        UUID = 'error'
    # TODO: закрыть уязвимость: возможность загружать файлы любого размера и любого расширения


    # TODO: закрыть уязвимость: проверять есть ли возможность сохранить
        # вначале сохранять и возврящать значение в зависимости от результата сохранения в бд
    size = 0
    try:
        _, file_extension = os.path.splitext(myFile.filename)

        if not file_extension in ['.doc', '.docx', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.kum', '.py']:
            return {"error":f"Недопустимое расширение файла",}
        
        with open(_USER_PATH+f"{UUID}_{task}{file_extension}", 'wb') as out:
            while True:
                data = myFile.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)
        answ = f"{UUID}_{task}{file_extension}"
        return tbl_set_answ(UUID, str(task), answ)
    except:
        return {"error": f"Файл не загружен"}




    if task.isdigit():
        task = int(task)
    else:
        task = 1
    
    sql = f'''
    UPDATE tests 
       SET 
        T_{task}_ANSW = (?),
        T_{task}_ANSW_TIME = (?)
     WHERE UUID = (?) and LOCK = 0;
    '''
    try:
        with sqlite3.connect(_DB_PATH) as db:
            answ_time = datetime.datetime.today()
            db.execute(sql, (answ, answ_time, UUID,))
        return {
                        "ANSW_TIME": str(answ_time),
                    }
    except sqlite3.Error as e:
        print(f"Error executing SQL query: {e}")
        return {"TASK_TEXT": f"Error executing SQL query: {e}"}
    finally:
        db.close()


def generate_test(TEST):
    if not TEST in os.listdir(path=f'{_TEST_PATH}'):
        return {}
        
    if "win" in platform:
        result = subprocess.run(['python', f'{_TEST_PATH}{TEST}'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    else:
        result = subprocess.run(['python3', f'{_TEST_PATH}{TEST}'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    print(result.stdout, result.stderr)
    try:
        if "win" in platform:
            d = json.loads(result.stdout.decode('cp1251'))
        else:
            d = json.loads(result.stdout.decode('utf-8'))
        return d
    except:
        return None
    
    
def tbl_get_db():
    sql = f'''
    SELECT * FROM tests
    ORDER BY NAME, TIME_START DESC;
    '''
    with sqlite3.connect(_DB_PATH) as db:
        column = db.execute(sql)
        column_names = [desc[0] for desc in column.description]
        column = column.fetchall()
        
    data = [dict(zip(column_names, column[i])) for i in range(len(column))]
    
    print(data[0])
    
    return data
    
def tbl_get_headers():
    sql_0 = 'SELECT substring(TIME_START, 1, 10) FROM tests ORDER BY TIME_START DESC;'
    sql_1 = 'SELECT NUM FROM tests ORDER BY NUM;'
    sql_2 = 'SELECT ("NUM" || "--" || "LETTER") FROM tests ORDER BY NUM, LETTER;'
    sql_3 = 'SELECT ("NUM" || "--" || "LETTER" || "--" || "TEST") FROM tests ORDER BY NUM, LETTER, TEST;'
    sql_4 = 'SELECT TEST FROM tests ORDER BY TEST;'
    sql_5 = 'SELECT (substring(TIME_START, 1, 10) || "--" || "NUM" || "--" || "LETTER" || "--" || "TEST") FROM tests ORDER BY TIME_START DESC, NUM, LETTER, TEST;'
    with sqlite3.connect(_DB_PATH) as db: 
        db.row_factory = lambda cursor, row: row[0]
        d0 = dict(Counter(db.execute(sql_0).fetchall()))
        d1 = dict(Counter(db.execute(sql_1).fetchall()))
        d2 = dict(Counter(db.execute(sql_2).fetchall()))
        d3 = dict(Counter(db.execute(sql_3).fetchall()))
        d4 = dict(Counter(db.execute(sql_4).fetchall()))
        d5 = dict(Counter(db.execute(sql_5).fetchall()))
    return {
        0:d0,
        1:d1,
        2:d2,
        3:d3,
        4:d4,
        5:d5,
    }

def tbl_get_results(TIME_START, NUM, LETTER, TEST):
    sql = f'''
    SELECT *
      FROM tests
     WHERE TIME_START LIKE (?) || "%" AND 
           NUM LIKE (?) AND 
           LETTER LIKE (?) AND 
           TEST LIKE (?) 
     ORDER BY NUM,
              LETTER,
              NAME,
              TEST,
              TIME_START DESC;
    '''
    with sqlite3.connect(_DB_PATH) as db:
        column = db.execute(sql, (TIME_START, NUM, LETTER, TEST,))
        column_names = [desc[0] for desc in column.description]
        column = column.fetchall()  
    data = [dict(zip(column_names, column[i])) for i in range(len(column))]
    return data


'''    
    
def get_40_tests(TEST):
    # Преднастройка документа и парсера html
    document = Document()
    new_parser = HtmlToDocx()
    section = document.sections[0]
    section.left_margin = Mm(12.7)
    section.right_margin = Mm(12.7)
    section.top_margin = Mm(12.7)
    section.bottom_margin = Mm(12.7)
    # генерация 40 вариантов
    sres = ''
    s = ''
    var = 1  
    while var <= 40:
        document.add_paragraph(f'Вариант {var}\n')
        sres += f"\nОтветы. Вариант {var}\n"
        test1 = generate_test(TEST)
        for i in range(1, 1+test1['COUNT']):
            html = f'{i}. '+test1[f'T_{i}_TEXT']
            new_parser.add_html_to_document(html, document)
            sres += f' {i}.'+test1[f'T_{i}_ANSW_CORRECT']
        document.add_page_break()
        var += 1
    document.add_paragraph(sres)
    
    # сохраняем в поток
    target_stream = BytesIO()
    document.save(target_stream)
    print('готово')
    return target_stream.getvalue()
'''


def tbl_backup():
    backup_file = _DB_PATH+'.backup.db'
    db_file = _DB_PATH
    try:
        if os.path.exists(backup_file):
            os.remove(backup_file)

        with sqlite3.connect(db_file) as source:
            with sqlite3.connect(backup_file) as target:
                source.backup(target)
        return True
    except:
        return False
    finally:
        source.close()
        target.close()
        
        
def get_test_py(TEST):
    if not TEST in os.listdir(path=f'{_TEST_PATH}'):
        return {}
    
    with open(f'{_TEST_PATH}{TEST}', encoding="utf-8") as code:
        return code.read()
        
def save_test_py(TEST, CODE):
    with open(f'{_TEST_PATH}{TEST}', 'w', encoding="utf-8") as code:
        code.write(decodeURIComponent(CODE))
    return {"TIME_SAVE": f"{datetime.datetime.today()}"}
        
def del_test_py(TEST):
    try:
        os.rename(f'{_TEST_PATH}{TEST}', f'{_TEST_PATH}_{TEST}')
        print(f"Файл {TEST} скрыт успешно.")
    except OSError as e:
        print(f"Ошибка при скрытии файла {TEST}: {e}")


if __name__ == "__main__":
    print(tbl_backup())


