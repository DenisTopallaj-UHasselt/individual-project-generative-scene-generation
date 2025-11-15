#!/bin/bash

PROJECT_DIR="${PROJECT_DIR:-$HOME/Desktop/UHasselt/individual-project}" # will be changed in the docker image

"$PROJECT_DIR/LichtFeld-Studio/build/LichtFeld-Studio" \
	-d "$PROJECT_DIR/pipeline/new_model/colmap_project/" \
	-o "$PROJECT_DIR/LichtFeld-Studio/output/mustang2/" \
	--gut
