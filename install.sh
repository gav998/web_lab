#!/usr/bin/env bash

# Получаем имя текущего пользователя
echo "USER_NAME=$(whoami)"
USER_NAME=$(whoami)

# Получаем директорию, где лежит скрипт
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
echo "SCRIPT_DIR=$SCRIPT_DIR"

# Запрашиваем пароль для JupyterLab
echo "Enter password for JupyterLab admin panel:"
read -s password

# Создаем виртуальное окружение
echo "Creating virtual environment..."
python3 -m venv --system-site-packages "${SCRIPT_DIR}/venv_weblab"

# Активируем виртуальное окружение
source "${SCRIPT_DIR}/venv_weblab/bin/activate"

# Устанавливаем необходимые системные пакеты
echo "Installing system requirements..."
sudo apt-get update
sudo apt-get -y install gcc python3-dev
sudo apt -y install git

echo "Installing python requirements from requirements.txt..."
pip install -r "${SCRIPT_DIR}/requirements.txt"

JUPYTER_PASSWORD_HASH=$(python -c "from jupyter_server.auth import passwd; print(passwd('$password'))")



# Создаем сервис автозапуска JupyterLab 8888
SERVICE_FILE="/etc/systemd/system/jupyterlab.service"
echo "Creating systemd service at $SERVICE_FILE..."
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=JupyterLab Autostart
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'sleep 5 && source "${SCRIPT_DIR}/venv_weblab/bin/activate" && jupyter lab --ip=0.0.0.0 --no-browser --NotebookApp.password='\''$JUPYTER_PASSWORD_HASH'\'
WorkingDirectory=${SCRIPT_DIR}
User=${USER_NAME}

[Install]
WantedBy=default.target
EOF

# Включаем и запускаем сервис
sudo systemctl stop jupyterlab.service
sudo systemctl disable jupyterlab.service
sudo systemctl daemon-reload
sudo systemctl enable jupyterlab.service
sudo systemctl start jupyterlab.service



# Создаем сервис автозапуска server 9090
SERVICE_FILE="/etc/systemd/system/server.service"
echo "Creating systemd service at $SERVICE_FILE..."
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=server Autostart
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'sleep 5 && source "${SCRIPT_DIR}/venv_weblab/bin/activate" && python "${SCRIPT_DIR}/server/server.py"'
WorkingDirectory=${SCRIPT_DIR}/server
User=${USER_NAME}
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=default.target
EOF

# Включаем и запускаем сервис
sudo systemctl stop server.service
sudo systemctl disable server.service
sudo systemctl daemon-reload
sudo systemctl enable server.service
sudo systemctl start server.service



# Создаем сервис автозапуска ngrok
# SERVICE_FILE="/etc/systemd/system/ngrok.service"
# echo "Creating systemd service at $SERVICE_FILE..."
# sudo bash -c "cat > $SERVICE_FILE" <<EOF
# [Unit]
# Description=ngrok Autostart
# After=network.target

# [Service]
# Type=simple
# ExecStart=/bin/bash -c 'sleep 5 && ngrok start --all --config="${SCRIPT_DIR}/ngrok.yml"'
# WorkingDirectory=${SCRIPT_DIR}
# User=${USER_NAME}
# Restart=on-failure
# RestartSec=5s

# [Install]
# WantedBy=default.target
# EOF

# Включаем и запускаем сервис
# sudo systemctl stop ngrok.service
# sudo systemctl disable ngrok.service
# sudo systemctl daemon-reload
# sudo systemctl enable ngrok.service
# sudo systemctl start ngrok.service



# Создаем сервис автозапуска update_ip_config_server
SERVICE_FILE="/etc/systemd/system/update_ip_config_server.service"
echo "Creating systemd service at $SERVICE_FILE..."
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=update_ip_config_server Autostart
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'sleep 5 && source "${SCRIPT_DIR}/venv_weblab/bin/activate" && python "${SCRIPT_DIR}/run_ngrok.py"'
WorkingDirectory=${SCRIPT_DIR}
User=${USER_NAME}
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=default.target
EOF

# Включаем и запускаем сервис
sudo systemctl stop update_ip_config_server.service
sudo systemctl disable update_ip_config_server.service
sudo systemctl daemon-reload
sudo systemctl enable update_ip_config_server.service
sudo systemctl start update_ip_config_server.service