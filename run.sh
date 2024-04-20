#!/bin/sh

cd /home/pimedia/mtvwebsocket/

if [ -n "$VIRUTAL_ENV" ]; then
    cd ./mtv_websocket_server
    python3 mtvwebsocketserver.py
    echo "Venv activated\nStarting server"
else
    source ./bin/activate
    cd ./mtv_websocket_server
    python3 mtvwebsocketserver.py
    echo "Venv activated\nStarting server"
fi

