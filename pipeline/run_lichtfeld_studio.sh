#!/bin/bash

PROJECT_DIR="${PROJECT_DIR:-$HOME/Desktop/UHasselt/individual-project}" # will be changed in the docker image

"$PROJECT_DIR/LichtFeld-Studio/build/LichtFeld-Studio" \
	-d "$PROJECT_DIR/pipeline/colmap_project_office/" \
	-o "$PROJECT_DIR/LichtFeld-Studio/output/office/" \
	--gut
