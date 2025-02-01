import os
import mimetypes
import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json

MOVIE_DIR = r"D:\Movies"

class MovieHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/movies":
            try:
                # List only directories (movie folders)
                movies = [d for d in os.listdir(MOVIE_DIR) if os.path.isdir(os.path.join(MOVIE_DIR, d))]
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(movies).encode())
            except Exception as e:
                print(f"Error: {e}")
                self.send_error(500, "Internal Server Error")

        elif self.path.startswith("/movies/"):
            # Decode URL-encoded folder name
            folder_name = urllib.parse.unquote(self.path[len("/movies/"):])
            folder_path = os.path.join(MOVIE_DIR, folder_name)

            if os.path.isdir(folder_path):
                # Find the first video file inside the folder
                video_files = [f for f in os.listdir(folder_path) if f.endswith((".mp4", ".mkv", ".avi"))]
                if video_files:
                    movie_path = os.path.join(folder_path, video_files[0])
                    mime_type, _ = mimetypes.guess_type(movie_path)
                    
                    if mime_type is None:
                        mime_type = "video/mp4"  # Default to MP4 if unknown
                    
                    self.send_response(200)
                    self.send_header("Content-Type", mime_type)
                    self.end_headers()
                    
                    with open(movie_path, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self.send_error(404, "No video file found in folder")
            else:
                self.send_error(404, "Movie folder not found")

        else:
            super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    server = HTTPServer(("0.0.0.0", 8000), MovieHandler)
    print("Server running at http://localhost:8000")
    server.serve_forever()
