#!/bin/bash

# Check if arguments is provided and 'user' | 'favorite' | 'authentication'
if [ $# -eq 0 ]; then
    echo "Script usage: $0 <destination: 'user' | 'favorite' | 'authentication'>"
    return 1
fi

case "$1" in
    "favorite")
        destination="./apps/microservices/favorite"
        ;;
    "authentication")
        destination="./apps/microservices/authentication"
        ;;
    "user")
        destination="./apps/microservices/user"
        ;;
    *)
        echo "Destination '$1' invalid.\nChoose either 'user' | 'favorite' | 'authentication'"
        return 1
        ;;
esac

cp -r database_access_layer $destination
echo "DAL Folder copied into microservice $1"

return 0