# Pipeline

## File/folders explanation

- [data](data): docker mounts here to retrieve your video
- [./install_colmap.sh](install_colmap.sh): clones and builds the COLMAP project
- [./pipeline_colmap.sh](pipeline_colmap.sh): uses the COLMAP project on your
  video. The video will be cut using ffmpeg based on the frames you give in. The
  files created will be placed in a directory you provide
    - video_file: the video file located in your ./data folder. Default is "output.mp4"
    - project_dir: the name of the directory you want your colmap project to
      place the files after using your images. Default is "colmap_project"
    - fps: frames per second you want ffmpeg to cut your video. Default is 30
    - max_frames: maximum number of frames to extract (prevents too many
      frames). Default is 300.
    - Ex.: `./pipeline_colmap.sh /data/output3.mp4 colmap_project 10`
- [./run_lichtfeld_studio](run_lichtfeld_studio.sh): runs the LichtFeld-Studio
  project using your created COLMAP project (from the previous command) and given
  an output folder, it places the .ply files in it.
    - The "colmap_project" directory is hard coded

## Docker Container

```bash
Usage: ./lichtfeld_docker.sh [-u] [-c] [-d] [-e COMMAND] [-h]
  -u       Start container (docker-compose up)
  -d       Stop container (docker-compose down)
  -c       Clean ouput directories
  -e CMD   Execute command in running container
  -s       Enter container shell
  -h       Show this help message

Examples:
  ./lichtfeld_docker.sh -u                              # Start container
  ./lichtfeld_docker.sh -e ./run_lichtfeld_studio.sh    # Run studio
  ./lichtfeld_docker.sh -c                              # Clean output directories
  ./lichtfeld_docker.sh -e './pipeline_colmap.sh /data/video.mp4 output 10'  # Run pipeline
  ./lichtfeld_docker.sh -s                              # Enter container shell
  ./lichtfeld_docker.sh -d                              # Stop container
```
