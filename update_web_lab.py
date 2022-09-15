import os 
from sys import platform
import subprocess

os.system("git clone https://github.com/gav998/web_lab.git ../web_lab_temp")

b = [
    "/update_web_lab.py",
    "/config_ftp.txt",
    "/client/conf.js",
    "/server/data.db",
    "/server/KEY.txt",
    "/server/tests/",
    "/.git/",
    "/.obsidian/",
    "__pycache__",
    ]

f = []

for (dirpath, dirnames, filenames) in os.walk('../web_lab_temp'):
    for filename in filenames:
        n = dirpath+'/'+filename
        n = n.replace('\\', '/')
        
        if any([True for i in range(len(b)) if b[i] in n]):
            continue
        f.append(n)

if "win" in platform: 
    for file in f:
        filename = file.replace('/', '\\')
        cmd = f'copy /Y "{filename}" "{"."+filename[15:]}"'
        p = subprocess.Popen(cmd, shell = True)
    p.wait()
    os.system(f'rd /s /q "../web_lab_temp/"')
else:
    for file in f:
        os.system(f'cp {file} {""+file[15:]}')
    os.system(f'rm -rf "../web_lab_temp/"')
    


