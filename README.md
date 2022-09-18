# Description
A service for testing students.
Tests in the Python programming language are automatically generated.

The application consists of a client (HTMP5, Bootstrap only JS).
The client can be hosted on a static file server.

The server is a set of API functions for client interaction with the database and execution of tests.

The server can be run on a local computer, for example raspberry pi.

An intermediary, ngrok, is used to determine the server address.

The service is provided as is, for personal use.

<img src="https://github.com/gav998/web_lab/blob/main/photo_2022-09-03_23-17-04.jpg" height="200"> <img src="https://github.com/gav998/web_lab/blob/main/photo_2022-09-03_23-17-06.jpg" height="200"> <img src="https://github.com/gav998/web_lab/blob/main/photo_2022-09-03_23-17-08.jpg" height="200"> <img src="https://github.com/gav998/web_lab/blob/main/2022-09-18_13-02-34.png" height="200"> <img src="https://github.com/gav998/web_lab/blob/main/2022-09-18_11-15-02.png" height="200"> 

# Setup
1. Copy Project
```bash
git clone https://github.com/gav998/web_lab.git
```

2. Install `cherrypy`
```bash
pip3 install cherrypy
```

**If you are using a testing system on a local network** (even without the Internet) (students' computers are clients; teachers' computer is a server), you need to follow step 3.

**If you use only one dedicated server**, then you need to open several ports: 80 for the client and 9090 for the API server.

3. Enter the address of your server in the file `./client/conf.js`

**If you have a gray, dynamic ip**, you need to follow steps 4-6.
At the moment, the server is an API only. This solution is suitable if you have a dedicated HTML server.

4. Install and base config `ngrok` from site [ngrok - download](https://ngrok.com/download) 
For Windows you need copy ngrok.exe in project folder

5. Edit file `config_ftp.txt`
```text
ftp://your_server.com/http/
your_FTP_login
your_FTP_password
```

6. Upload the `client` folder to your HTML hosting.
You may upload manually or run `upload_client_ftp.py` 

# Autorun / start
For autorun use `cron` with command
```bash
crontab -e
```

1. **If you have a WHITE, STATIC IP** add line: (user - pi) (terminal - lxterminal):
```bash
@reboot sleep 20 && export DISPLAY=:0 && cd /home/pi/web_lab/server/ && sudo -u pi lxterminal -e python3 server.py
```
For start manually you may run `server.py` 

**If you want to receive updates** every week (at 7 am on Saturday) add line:
```bash
0 7 * * 6 sleep 20 && export DISPLAY=:0 && cd /home/pi/web_lab/ && sudo -u pi lxterminal -e python3 update_web_lab.py
```
For update manually you may run `update_web_lab.py` 

---
2. **If you have a GRAY, DYNAMIC IP** add line: 
```bash
@reboot sleep 20 && export DISPLAY=:0 && cd /home/pi/web_lab/ && sudo -u pi lxterminal -e python3 run_ngrok.py 
@reboot sleep 20 && export DISPLAY=:0 && cd /home/pi/web_lab/server/ && sudo -u pi lxterminal -e python3 server.py
```
Or run manually `run_ngrok.py` and `server.py` 

**If you want to receive updates** every week (at 7 am on Saturday) add line:

```bash
0 7 * * 6 sleep 20 && export DISPLAY=:0 && cd /home/pi/web_lab/ && sudo -u pi lxterminal -e python3 update_web_lab.py && sudo -u pi lxterminal -e python3 upload_client_ftp.py
```
Or run manually `update_web_lab.py` and `upload_client_ftp.py` 

# Add test
Edit and create file.py in folder ./server/tests/ from examples.
There is a limit of 30 questions per test.

# Checking the tests
Visit the page your-server.com/result.html?KEY=your_key_in_the_file_./server/KEY.txt

# Description of executable files
`update_web_lab.py` - update project from github, excluding files:
- ./update_web_lab.py
- ./config_ftp.txt
- ./client/conf.js
- ./server/data.db
- ./server/KEY.txt
- ./server/tests/*

`upload_client_ftp.py` - upload client to HTML host excluding ./client/conf.js 

`run_ngrok.py` - run ngrok, update and upload to HTML host ./client/conf.js. This is an iterative process

`upload_conf_ftp.py` - upload to HTML host ./client/conf.js

`server.py` - run API server
