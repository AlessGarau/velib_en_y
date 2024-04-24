#!/bin/bash

MICROSERVICES_DIR=./apps/microservices

copy_db_access_into() {
    cp -r database_access_layer $MICROSERVICES_DIR$1
    echo "DAL Folder copied into $1 folder"
}

# Check if arguments is provided and is 'user' | 'favorite' | 'authentification'
if [ $# -eq 0 ]; then
    echo "Script usage: $0 <destination: 'user' | 'favorite' | 'authentification'>"
    return 1
fi

case "$1" in
    "favorite")
        copy_db_access_into "/favorite"
        ;;
    "authentification")
        copy_db_access_into "/authentification"
        ;;
    "user")
        copy_db_access_into "/user"
        ;;
    *)
        echo "Destination '$1' invalid.\nChoose either 'user' | 'favorite' | 'authentification'"
        return 1
        ;;
esac
