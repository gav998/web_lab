import datetime
import sqlite3
import os
import subprocess
import json
from sys import platform


CURR_PATH = os.path.abspath(os.getcwd())
DB_PATH = CURR_PATH + "/data.db"
#DB_PATH = CURR_PATH + "\data.db"

 
def tbl_new_uuid(UUID, TEST, NAME, NUM, LETTER): 
    test = generate_test(TEST) 
    sql = f'''
    INSERT 
      INTO tests(UUID, TEST, NAME, NUM, LETTER, TIME_START, {', '.join(list(test.keys()))}) 
    VALUES (?, ?, ?, ?, ?, ?, {', '.join(['?' for i in list(test.keys())])});    
    ''' 
    values = [UUID, TEST, NAME, NUM, LETTER, datetime.datetime.today()]  
    values.extend(test.values())
    values = tuple(values)
    with sqlite3.connect(DB_PATH) as db:
        db.execute(sql, values)
    return {
                "UUID": UUID,
           }
        
def tbl_get_test(UUID, TASK):
    sql = '''
    SELECT * FROM tests WHERE UUID = (?);
    '''   
    with sqlite3.connect(DB_PATH) as db:
        column = db.execute(sql, (UUID,))
        column_names = [desc[0] for desc in column.description]
        column = column.fetchone()
        test = dict(zip(column_names, column))
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
                    "ANSW": test["T_"+TASK+"_ANSW"],
                    "ANSW_TIME": test["T_"+TASK+"_ANSW_TIME"],
                    
                }

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
    with sqlite3.connect(DB_PATH) as db:
        db.execute(sql1, (UUID,)).fetchone()
        column = db.execute(sql2, (UUID,))
        column_names = [desc[0] for desc in column.description]
        column = column.fetchone()
        test = dict(zip(column_names, column))
    return test

     
def tbl_set_answ(UUID, task, answ):
    sql = f'''
    UPDATE tests 
       SET 
        T_{int(task)}_ANSW = (?),
        T_{int(task)}_ANSW_TIME = (?)
     WHERE UUID = (?) and LOCK = 0;
    '''
    with sqlite3.connect(DB_PATH) as db:
        answ_time = datetime.datetime.today()
        db.execute(sql, (answ, answ_time, UUID,))
    return {
                    "ANSW_TIME": str(answ_time),
                }


def generate_test(TEST):
    if not TEST in os.listdir(path='./tests'):
        return {}
        
    if "win" in platform:
        result = subprocess.run(['python', f'./tests/{TEST}'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    else:
        result = subprocess.run(['python3', f'./tests/{TEST}'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    
    if "win" in platform:
        d = json.loads(result.stdout.decode('cp1251'))
    else:
        d = json.loads(result.stdout.decode('utf-8'))

    return d
