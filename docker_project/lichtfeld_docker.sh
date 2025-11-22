#!/bin/bash

usage() {
	echo "Usage: $0 [-u] [-c] [-d] [-e COMMAND] [-h]"
	echo "  -u       Start container (docker-compose up)"
	echo "  -d       Stop container (docker-compose down)"
	echo "  -c       Clean ouput directories"
	echo "  -e CMD   Execute command in running container"
	echo "  -s       Enter container shell"
	echo "  -h       Show this help message"
	echo ""
	echo "Examples:"
	echo "  $0 -u                              # Start container"
	echo "  $0 -e ./run_lichtfeld_studio.sh    # Run studio"
	echo "  $0 -c                              # Clean output directories"
	echo "  $0 -e './pipeline_colmap.sh /data/video.mp4 output 10'  # Run pipeline"
	echo "  $0 -s                              # Enter container shell"
	echo "  $0 -d                              # Stop container"
}

COMPOSE_FILE="docker-compose.yml"

# Export environment variables for docker-compose
export DISPLAY=$DISPLAY
export XAUTHORITY=$XAUTHORITY
export HOME=$HOME
export PWD=$(pwd)

# Parse options
while getopts "ucde:sh" opt; do
	case ${opt} in
	u)
		echo "Starting lichtfeld-studio container..."
		xhost +local:docker
		docker compose -f $COMPOSE_FILE up -d
		if [ $? -eq 0 ]; then
			echo "Container started successfully!"
			echo "Use '$0 -e \"./scripts/pipeline_colmap.sh /data/output3.mp4 colmap_project 10\" to run the pipeline"
			echo "Use '$0 -e ./run_lichtfeld_studio.sh' to run the studio"
			echo "Use '$0 -s' to enter the container"
		fi
		;;
	c)
		echo "Cleaning project directories..."
		sudo rm -rf ./colmap_project/* 2>/dev/null || true
		sudo rm -rf ./data/colmap_project/* 2>/dev/null || true
		echo "Cleaned successfully!"
		;;
	d)
		echo "Stopping lichtfeld-studio container..."
		docker compose -f $COMPOSE_FILE down
		xhost -local:docker
		;;
	e)
		COMMAND="$OPTARG"
		echo "Executing: $COMMAND"
		docker compose -f $COMPOSE_FILE exec lichtfeld-studio bash -c "$COMMAND"
		;;
	s)
		echo "Entering container shell..."
		docker compose -f $COMPOSE_FILE exec lichtfeld-studio bash
		;;
	h)
		usage
		exit 0
		;;
	*)
		usage
		exit 1
		;;
	esac
done

# If no arguments provided, show usage
if [ $OPTIND -eq 1 ]; then
	usage
	exit 1
fi
