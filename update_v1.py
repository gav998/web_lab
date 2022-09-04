import os 


def get_files():
    print("get_files")
    os.system("curl -L https://github.com/gav998/web_lab/raw/main/server/server.py --ssl-no-revoke > ./server/server.py")
    os.system("curl -L https://github.com/gav998/web_lab/raw/main/server/utils.py --ssl-no-revoke > ./server/utils.py")
    
    os.system("curl -L https://github.com/gav998/web_lab/raw/main/run.py --ssl-no-revoke > ./run.py")
    
    os.system("curl -L https://github.com/gav998/web_lab/raw/main/client/index.html --ssl-no-revoke > ./client/index.html")
    os.system("curl -L https://github.com/gav998/web_lab/raw/main/client/test.html --ssl-no-revoke > ./client/test.html")
    os.system("curl -L https://github.com/gav998/web_lab/raw/main/client/result.html --ssl-no-revoke > ./client/result.html")
    
    print("OK")
    
   
get_files()