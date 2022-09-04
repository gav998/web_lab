# Setup

## If you don't have a static IP
1. Copy Project
```bash
git clone https://github.com/gav998/web_lab.git
```

2. Install and base config `ngrok` from site [ngrok - download](https://ngrok.com/download) 

For Win:
Copy ngrok.exe in project folder

3. Install `cherrypy`
```bash
pip3 install cherrypy
```

4. Edit file `config_ftp.txt`
```text
ftp://your_server.com/http/
your_FTP_login
your_FTP_password
```

5. Setup autorun file `run.py` (execute as non sudo)
```bash
crontab -e
```
add line in script (user - pi) (terminal - lxterminal)
```bash
@reboot sleep 20 && export DISPLAY=:0 && cd /home/pi/web_lab/ && sudo -u pi lxterminal -e python3 update_v1.py && sudo -u pi lxterminal -e python3 run.py
```

## If you have a static IP (or local start)

1. Copy Project
```bash
git clone https://github.com/gav998/web_lab.git
```

2. Edit file `./client/conf.js` 
Enter your server address. if you start project in local machine don't edit file.

3. Upload folder `client` for your HTML hosting.

4. Setup autorun file `./server/server.py` for server (execute as non sudo)

# Add test
Edit and create file.py in folder ./server/tests/ from examples.
There is a limit of 30 questions per test.

# Description
A service for testing students.
Tests in the Python programming language are automatically generated.

The application consists of a client (HTMP5, Bootstrap only JS).
The client can be hosted on a static file server.

The server is a set of API functions for client interaction with the database and execution of tests.

The server can be run on a local computer, for example raspberry pi.

An intermediary, ngrok, is used to determine the server address.

The service is provided as is, for personal use.

<img src="https://github.com/gav998/web_lab/blob/main/photo_2022-09-03_23-17-04.jpg" height="200"> <img src="https://github.com/gav998/web_lab/blob/main/photo_2022-09-03_23-17-06.jpg" height="200"> <img src="https://github.com/gav998/web_lab/blob/main/photo_2022-09-03_23-17-08.jpg" height="200">
# Описание
Сервис для тестирования учащихся.
Автоматически генерируются тесты на языке программирования Python.

Приложение состоит из клиента (HTMP5, Bootstrap JS only).
Клиент может быть размещен на статичном файловом сервере.
Настройки FTP необходимы для обновления адреса сервера

Сервер представляет собой набор API функций для взаимодействия клиента с базой данных и исполнения тестов.

Сервер может быть запущен на локальном компьютере, например raspberry pi.

Для определения адреса сервера используется посредник - ngrok.

Сервис предоставляется как есть, для личного использования.

