import os 
import json
import datetime
import time
import subprocess
from sys import platform


def get_tunnels():
    print("get_tunnels")
    os.system("curl  http://localhost:4040/api/tunnels > ./tunnels.json")

    with open('./tunnels.json', 'rt') as data_file:
        j = data_file.read()
    if len(j)==0:
        print('tunnels.json empty')
        return False
    j = json.loads(j)
    if 'tunnels' in j and len(j['tunnels'])>0 and 'public_url' in j['tunnels'][0]:
        print('tunnels.json OK')
        return j['tunnels'][0]['public_url']+'/'
    else:
        print('tunnels.json unknown')
        return False

def start_tunnels():
    print("start_tunnels")
    if "win" in platform:
        proc = subprocess.Popen("ngrok http 9090", shell=True)
    else:
        proc = subprocess.Popen("lxterminal -e ngrok http 9090", shell=True)
    time.sleep(5)
    update_conf(get_tunnels())
    return proc


def start_serv():
    print("start_serv")
    if "win" in platform:
        subprocess.Popen("cd ./server/ && python ./server.py", shell=True)
    else:
        subprocess.Popen("cd ./server/ && lxterminal -e python3 ./server.py", shell=True)
    time.sleep(5)


def restart_tunnels():
    print("restart_tunnels")
    global proc
    proc.terminate()
    time.sleep(5)
    proc = start_tunnels()
    time.sleep(5)


def update_conf(tunnels):
    print("update_conf")
    with open('./client/conf.js', "a") as conf_file:
        conf_file.write(f"// {datetime.datetime.today()}\n")
        conf_file.write(f'server = "{tunnels}"\n\n')
    os.system(f"curl -T ./client/conf.js {ftp} --user {user}:{password}")
    
    
def update_client():
    print("update_client")
    os.system(f"curl -T ./client/conf.js {ftp} --user {user}:{password}")
    os.system(f"curl -T ./client/index.html {ftp} --user {user}:{password}")
    os.system(f"curl -T ./client/test.html {ftp} --user {user}:{password}")
    os.system(f"curl -T ./client/result.html {ftp} --user {user}:{password}")
    

with open('./config_ftp.txt') as config_ftp:
    ftp=config_ftp.readline().rstrip()
    user=config_ftp.readline().rstrip()
    password=config_ftp.readline().rstrip()
    print(f'{ftp} {user} {password}')
    time.sleep(1)


start_serv()
update_client()
proc = start_tunnels()
time.sleep(5)

while True:
    tunnels = get_tunnels()
    print(tunnels)
    if not tunnels:
        print(datetime.datetime.today(), "tunnels NOT EXIST")
        restart_tunnels()
    else:
        print(datetime.datetime.today(), "OK", tunnels)
        time.sleep(10)
