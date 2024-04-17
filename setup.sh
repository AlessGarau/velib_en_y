#!/bin/bash

PYTHON=python3
PIP=pip3
FLASK_RUN="$PYTHON -m flask run"
WEB_SERVER_DIR=apps/velyb-web-server
API_CACHE_DIR=apps/api-caching-server
MICROSERVICES_DIR=apps/microservices

print_help() {
	echo "Available actions:"
	echo "  install                Install dependencies"
	echo "  run-api-cache          Run the API caching server"
	echo "  run-velyb-web-server   Run the velyb web server"
	echo "  run-microservices      Run the microservices"
}

create_and_activate_venv() {
	$PYTHON -m venv velyb
	source velyb/bin/activate
}

install_dependencies() {
	$PIP install -r requirements.txt
}

run_api_cache_server() {
	cd $API_CACHE_DIR && $PYTHON app.py
}

run_velyb_web_server() {
	cd $WEB_SERVER_DIR && $FLASK_RUN --port 8000
}

run_microservices() {
	cd $MICROSERVICES_DIR/authentification && $FLASK_RUN --port 8001 &
	cd $MICROSERVICES_DIR/favorite && $FLASK_RUN --port 8002 &
	cd $MICROSERVICES_DIR/user && $FLASK_RUN --port 8003 &
}

run_all() {
	install_dependencies
	run_api_cache &
	run_velyb_web_server &
	run_microservices
}

stop_all() {
	pkill -f "flask run" &
	pkill -f "python app.py"
}

case "$1" in
venv)
	create_and_activate_venv
	;;
install)
	install_dependencies
	;;
run-api-cache)
	run_api_cache_server
	;;
run-velyb-web-server)
	run_velyb_web_server
	;;
run-microservices)
	run_microservices
	;;
all)
	run_all
	;;
*)
	print_help
	;;
esac
