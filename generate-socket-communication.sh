#!/bin/bash

ROOT_DIR=./apps

copy_socket_communication_into() {
    cp -r socket_communication "$ROOT_DIR$1"
    echo "DAL Folder copied into $1 folder"
}

if [ $# -eq 0 ]; then
    echo "Script usage: $0 <destination: 'velyb-web-server' | 'api-caching-server'>"
    return 1
fi

case "$1" in
    "velyb-web-server")
        copy_socket_communication_into "/velyb-web-server"
        ;;
    "api-caching-server")
        copy_socket_communication_into "/api-caching-server"
        ;;
    *)
        echo "Destination '$1' invalid. Choose either 'velyb-web-server' or 'api-caching-server'"
        return 1
        ;;
esac
