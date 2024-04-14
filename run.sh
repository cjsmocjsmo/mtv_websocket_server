cd /home/pimedia/mtv_websocker_server

if [ -n "$VIRUTAL_ENV" ]; then
    python3 mtvwebsocketserver.py
    echo "Venv activated\nStarting server"
else
    source ./bin/activate
    python3 mtvwebsocketserver.py
    echo "Venv activated\nStarting server"
fi

