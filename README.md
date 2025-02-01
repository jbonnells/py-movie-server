# py-movie-server

## Overview
`py-movie-server` is a simple Python-based web server that serves a list of movies from a specified directory. Users can view the list of movies and play them directly in their web browser.

## Features
- Lists movie directories from a specified folder.
- Streams the first video file found in each movie directory.
- Supports video formats: `.mp4`, `.mkv`, and `.avi`.

## Requirements
- Python 3.x

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/jbonnells/py-movie-server.git
    cd py-movie-server
    ```

2. Ensure you have the required Python version installed.

## Usage
1. Set the `MOVIE_DIR` variable in [server.py](http://_vscodecontentref_/0) to the path of your movie directory:
    ```python
    MOVIE_DIR = r"D:\Movies"
    ```

2. Run the server:
    ```sh
    python server.py
    ```

3. Open your web browser and navigate to `http://localhost:8000` to view and play your movies.

## Remote Access
To access the movie server from another device on the same network:
1. Find the IP address of the machine running the server. You can do this by running the following command in the terminal (Windows):
    ```sh
    ipconfig
    ```
    Look for the `IPv4 Address` under your active network connection.

2. Open your web browser on the remote device and navigate to `http://<IP_ADDRESS>:8000`, replacing `<IP_ADDRESS>` with the IP address you found in the previous step.

## Project Structure
- [index.html](http://_vscodecontentref_/1): The front-end HTML file that displays the movie list and video player.
- [server.py](http://_vscodecontentref_/2): The back-end Python script that handles HTTP requests and serves movie files.
- [.gitignore](http://_vscodecontentref_/3): Git ignore file to exclude unnecessary files from version control.
- [README.md](http://_vscodecontentref_/4): This file.

## License
This project is licensed under the MIT License.