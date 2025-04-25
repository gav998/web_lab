import os 
import datetime

with open('./config_ftp.txt') as config_ftp:
    ftp=config_ftp.readline().rstrip()
    user=config_ftp.readline().rstrip()
    password=config_ftp.readline().rstrip()



serv = input("Input new url: ")

if serv[-1] != '/': serv += '/'
with open('./client/conf.js', "a") as conf_file:
    conf_file.write(f"// {datetime.datetime.today()}\n")
    conf_file.write(f'server = "{serv}";\n')




cmd = f"curl -T ./client/conf.js {ftp} --user {user}:{password}"
print(cmd)
os.system(cmd)

