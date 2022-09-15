import os 
from sys import platform
import subprocess

with open('./config_ftp.txt') as config_ftp:
    ftp=config_ftp.readline().rstrip()
    user=config_ftp.readline().rstrip()
    password=config_ftp.readline().rstrip()

b = [
    "/conf.js",
    ]

f = []

for (dirpath, dirnames, filenames) in os.walk('./client/'):
    for filename in filenames:
        n = dirpath+filename
        n = n.replace('\\', '/')
        if any([True for i in range(len(b)) if b[i] in n]):
            continue
        f.append(n)

for file in f:
    cmd = f"curl -T {file} {ftp} --user {user}:{password}"
    print(cmd)
    os.system(cmd)

