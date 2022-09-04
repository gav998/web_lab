import os 
from sys import platform
import subprocess

os.system("git clone https://github.com/gav998/web_lab.git ../web_lab_temp")

b = [
    "/update_web_lab.py",
    "/config_ftp.txt",
    "/client/conf.js",
    "/server/data.db",
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
        if (b[0] in n or
            b[1] in n or
            b[2] in n or
            b[3] in n or
            b[4] in n or
            b[5] in n or
            b[6] in n or
            b[7] in n):
            continue
        f.append(n)


if "win" in platform: 
    for file in f:
        filename = file.replace('/', '\\')
        cmd = f'copy /Y "{filename}" "{"."+filename[15:]}"'
        p = subprocess.Popen(cmd, shell = True)
else:
    for file in f:
        os.system(f'cp {file} {""+file[15:]}')

p.wait()
os.system(f'rd /s /q "../web_lab_temp/"')

