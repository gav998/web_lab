import os 
import json
import datetime
import time
import subprocess
from sys import platform


def start_tunnels():
    print("start_tunnels")
    if "win" in platform:
        proc = subprocess.Popen("start ngrok http 9090", shell=True)
    else:
        proc = subprocess.Popen("lxterminal -e ngrok http 9090", shell=True)
    time.sleep(5)
    return proc

def get_public_url():
    print("get_public_url")
    os.system("curl http://localhost:4040/api/tunnels > ./tunnels.json")
    

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
    print("restart_tunnels")
    global proc
    proc.terminate()
    time.sleep(5)
    proc = start_tunnels()
    public_url = get_public_url()
    update_conf(public_url)
    time.sleep(15)


def update_conf(public_url):
    print("update_conf")
    with open('./client/conf.js', "a") as conf_file:
        conf_file.write(f"// {datetime.datetime.today()}\n")
        conf_file.write(f'server = "{public_url}"\n\n')
    if "win" in platform:
        os.system("start python ./upload_conf_ftp.py")
    else:
        os.system("lxterminal -e python3 ./upload_conf_ftp.py")


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
