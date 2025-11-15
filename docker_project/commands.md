# Build the image

sudo docker build -t lichtfeld-studio .

# Run the pipeline

sudo docker run --name lichtfeld-run --gpus all -v $(pwd)/data:/data lichtfeld-studio ./pipeline_colmap.sh /data/output3.mp4 colmap_project 10

# Run LichtFeld Studio

sudo docker run --name lichtfeld-run --gpus all -v $(pwd)/data:/data lichtfeld-studio ./run_lichtfeld_studio.sh

# Interactive mode

sudo docker run --name lichtfeld-run --gpus all -it -v $(pwd)/data:/data lichtfeld-studio /bin/bash
