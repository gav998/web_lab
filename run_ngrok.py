import os 
import json
import datetime
import time
import subprocess
from sys import platform


def start_tunnels():
    # Функция для запуска туннелей с помощью ngrok

    print("start_tunnels")  # Вывод сообщения о начале работы функции
    
    # Определение операционной системы пользователя и запуск соответствующей команды
    if "win" in platform:
        # Если операционная система - Windows, запускаем ngrok с использованием команды 'start'
        # proc = subprocess.Popen("start ngrok http 9090", shell=True)
        proc = subprocess.Popen('start ngrok start --all --config="ngrok.yml', shell=True)
        
    else:
        # Для других ОС (например, Linux) используем lxterminal для запуска ngrok
        # proc = subprocess.Popen("lxterminal -e ngrok http 9090", shell=True)
        proc = subprocess.Popen(["ngrok", "start", "--all", "--config=ngrok.yml"])

    time.sleep(5)  # Ожидаем 5 секунд для установления соединения с ngrok
    
    return proc  # Возвращаем объект процесса, чтобы иметь возможность управлять им в дальнейшем


def get_public_url():
    # Функция для получения публичного URL из tunnels.json, который создается ngrok

    print("get_public_url")  # Вывод сообщения о начале работы функции
    
    # Получение данных о туннелях с помощью утилиты curl и сохранение их в файл tunnels.json
    os.system("curl -s http://localhost:4040/api/tunnels > ./tunnels.json")
    
    # Открытие файла tunnels.json для чтения
    with open('./tunnels.json', 'rt') as data_file:
        j = data_file.read()  # Чтение содержимого файла

    # Проверка на пустоту содержимого файла
    if len(j) == 0:
        print('tunnels.json empty')  # Сообщение пользователю о пустом файле
        return False  # Возврат False, если файл пустой

    j = json.loads(j)  # Конвертация строки с JSON-данными в Python словарь или список
    
    # Проверка наличия информации о туннелях и возврат публичного URL, если он существует
    if 'tunnels' in j and len(j['tunnels']) > 0 and 'public_url' in j['tunnels'][0]:
        print('tunnels.json OK')  # Сообщение о наличии необходимых данных
        tunnels = {
            j['tunnels'][0]['name']: j['tunnels'][0]['public_url'] + '/',
            j['tunnels'][1]['name']: j['tunnels'][1]['public_url'] + '/',
        }
        return tunnels  # Возврат публичного URL с добавлением слэша jupyter, weblab

    else:
        print('tunnels.json unknown')  # Сообщение пользователю о непредвиденной структуре файла
        return False  # Возврат False, если нужные данные не найдены



'''
def start_serv():
    print("start_serv")
    if "win" in platform:
        subprocess.Popen("cd ./server/ && python ./server.py", shell=True)
    else:
        subprocess.Popen("cd ./server/ && lxterminal -e python3 ./server.py", shell=True)
    time.sleep(5)
'''

def restart_tunnels():
    # Функция для перезапуска туннелей и обновления конфигурации с новым публичным URL

    print("restart_tunnels")  # Вывод сообщения о начале процесса перезапуска туннелей
    
    # Использование глобальной переменной proc, которая предположительно является процессом туннеля
    global proc
    proc.terminate()  # Завершение работы текущего процесса
    time.sleep(5)  # Ожидание в течение 5 секунд перед запуском нового процесса
    
    # Запуск новых туннелей и присваивание нового процесса глобальной переменной proc
    proc = start_tunnels()
    
    # Получение нового публичного URL с помощью функции get_public_url
    public_url = get_public_url()
    
    # Обновление конфигурации (файла настроек клиента) с новым публичным URL
    update_conf(public_url)
    
    time.sleep(15)  # Ожидание в течение 15 секунд для устойчивости работы системы



def update_conf(public_url):
    print("update_conf")
    with open('./client/conf.js', "a") as conf_file:
        conf_file.write(f"// {datetime.datetime.today()}\n")
        conf_file.write(f'server = "{public_url["weblab"]}";\n')
        conf_file.write(f'server_lab = "{public_url["jupyter"]}";\n\n')
    if "win" in platform:
        os.system("start python ./upload_conf_ftp.py")
    else:
        # os.system("lxterminal -e python3 ./upload_conf_ftp.py")
        os.system('source "venv_weblab/bin/activate" && python ./upload_conf_ftp.py')


proc = start_tunnels()
public_url=get_public_url() 
update_conf(public_url)
time.sleep(5)

while True:
    public_url = get_public_url()
    # print(public_url)
    if not public_url:
        print(datetime.datetime.today(), "public_url NOT EXIST")
        restart_tunnels()
    else:
        print(datetime.datetime.today(), "OK", public_url)
        time.sleep(10)
