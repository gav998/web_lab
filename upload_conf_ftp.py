import os 

with open('./config_ftp.txt') as config_ftp:
    ftp=config_ftp.readline().rstrip()
    user=config_ftp.readline().rstrip()
    password=config_ftp.readline().rstrip()

cmd = f"curl -T ./client/conf.js {ftp} --user {user}:{password}"
print(cmd)
os.system(cmd)
