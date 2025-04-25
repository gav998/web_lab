start cmd /k "clo publish http 127.0.0.1:9090"
start cmd /k "cd server & %USERPROFILE%/miniconda3/condabin/activate & conda activate web_lab && python server.py" 