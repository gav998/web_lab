#!/usr/bin/env bash

# Получаем имя текущего пользователя
USER_NAME=$(whoami)

# Получаем директорию, где лежит скрипт
SCRIPT_DIR=$(dirname "$0")

# Запрашиваем пароль
JUPYTER_PASSWORD_HASH=$(python -c "import getpass; from jupyter_server.auth import passwd; password = getpass.getpass('Enter password for JupyterLab admin panel: '); print(passwd(password))")


# Создаем виртуальное окружение
python -m venv --system-site-packages "${SCRIPT_DIR}/venv_weblab"
source "${SCRIPT_DIR}/venv_weblab/bin/activate"
sudo apt-get -y install gcc python3-dev 
pip install -r requirements.txt

# Создаем сервис автозапуска JupyterLab
echo """
[Unit]
Description=JupyterLab Autostart
After=network.target
[Service]
Type=simple
ExecStart=/bin/bash -c \"sleep 5 && source '${SCRIPT_DIR}/venv_weblab/bin/activate' && python -m jupyterlab --ip='*' --no-browser --NotebookApp.password=${JUPYTER_PASSWORD_HASH}\"
WorkingDirectory=${SCRIPT_DIR}
User=$USER_NAME
[Install]
WantedBy=default.target
""" | sudo tee /etc/systemd/system/jupyterlab.service > /dev/null
# Включаем и запускаем сервис
sudo systemctl daemon-reload
sudo systemctl enable jupyterlab.service
sudo systemctl start jupyterlab.service

# Создаем сервис автозапуска ngrok
echo """
[Unit]
Description=ngrok Autostart
After=network.target
[Service]
Type=simple
ExecStart=/bin/ngrok http 9090
WorkingDirectory=${SCRIPT_DIR}
User=$USER_NAME
Restart=on-failure
[Install]
WantedBy=default.target
""" | sudo tee /etc/systemd/system/ngrok.service > /dev/null
# Включаем и запускаем сервис
sudo systemctl daemon-reload
sudo systemctl enable ngrok.service
sudo systemctl start ngrok.service

# Создаем сервис автозапуска weblab
echo """
[Unit]
Description=WebLab Autostart
After=network.target
[Service]
Type=simple
ExecStart=/bin/bash -c \"sleep 5 && source '${SCRIPT_DIR}/venv_weblab/bin/activate' && cd server && python server.py\"
WorkingDirectory=${SCRIPT_DIR}
User=$USER_NAME
Restart=on-failure
[Install]
WantedBy=default.target
""" | sudo tee /etc/systemd/system/WebLab.service > /dev/null
# Включаем и запускаем сервис
sudo systemctl daemon-reload
sudo systemctl enable WebLab.service
sudo systemctl start WebLab.service