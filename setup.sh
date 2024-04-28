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
	echo "  all                    Run all the services at once"
	echo "  run-api-cache          Run the API caching server"
	echo "  run-velyb-web-server   Run the velyb web server"
	echo "  run-microservices      Run the microservices"
	echo "  clean                  Kills all processes related to the project"
}

clean_up() {
	echo "Clean up"
	lsof -ti :8000,8001,8002,8003,8004 | xargs kill
}
trap "clean_up" EXIT SIGINT SIGTERM INT

create_and_activate_venv() {
	$PYTHON -m venv velyb_env
	source velyb/bin/activate
}

install_dependencies() {
	$PIP install -r requirements.txt
}

run_api_cache_server() {
	cd $API_CACHE_DIR && $PYTHON app.py

	wait
}

run_velyb_web_server() {
	cd $WEB_SERVER_DIR && $PYTHON app.py

	wait
}

run_microservices() {
	original_dir=$(pwd)

	source generate-database-access-layer.sh favorite
	source generate-database-access-layer.sh authentification
	source generate-database-access-layer.sh user

	(
		cd $MICROSERVICES_DIR/authentification && $PYTHON app.py
	) &

	(
		cd $original_dir && cd $MICROSERVICES_DIR/favorite && $PYTHON app.py
	) &

	(
		cd $original_dir && cd $MICROSERVICES_DIR/user && $PYTHON app.py
	) &

	cd $original_dir

	wait
}

run_all() {
	create_and_activate_venv
	install_dependencies
	run_api_cache_server &
	run_velyb_web_server &
	run_microservices

	wait
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
clean)
	clean_up
	;;
*)
	print_help
	;;
esac

# Made with ❤ by heitzjulien & LTOssian

