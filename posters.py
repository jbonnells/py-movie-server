import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

def list_movie_folders(parent_dir):
    """Lists all movie directories numerically and returns a dictionary mapping numbers to folder names."""
    movie_folders = [folder for folder in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, folder))]
    
    if not movie_folders:
        print("No movie folders found.")
        return {}
    
    folder_map = {}
    print("Select a movie folder by number:")
    for i, folder in enumerate(movie_folders, 1):
        print(f"{i}: {folder}")
        folder_map[str(i)] = folder
    
    return folder_map

def fetch_movie_poster(folder_path, movie_title, movie_year, api_key, skip_existing=True):
    """Fetches and saves a movie poster in the given directory."""
    file_path = os.path.join(folder_path, "cover.jpg")
    
    if skip_existing and os.path.exists(file_path):
        # print(f"Skipping {movie_title} ({movie_year}) - cover already exists.")
        return
    
    print(f"Fetching poster for: {movie_title} ({movie_year})")
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_title}&y={movie_year}"
    response = requests.get(url).json()
    
    if response.get("Response") == "True":
        poster_url = response.get("Poster")
        if poster_url and poster_url != "N/A":
            img_data = requests.get(poster_url).content
            with open(file_path, "wb") as f:
                f.write(img_data)
            print(f"Poster saved as {file_path}")
        else:
            print(f"Poster not found for {movie_title} ({movie_year}).")
    else:
        print(f"Movie not found for {movie_title} ({movie_year}).")

def get_movie_poster_for_selected(parent_dir, api_key):
    """Lists directories, lets user select, and fetches posters for selected movies."""
    folder_map = list_movie_folders(parent_dir)
    if not folder_map:
        return
    
    selections = input("Enter the numbers of the folders you want to fetch posters for (comma-separated): ").split(',')
    selections = [s.strip() for s in selections if s.strip() in folder_map]
    
    if not selections:
        print("No valid selections made.")
        return
    
    for selection in selections:
        folder = folder_map[selection]
        folder_path = os.path.join(parent_dir, folder)
        match = re.match(r"(.+) \((\d{4})\).*", folder)
        
        if match:
            movie_title, movie_year = match.groups()
            fetch_movie_poster(folder_path, movie_title, movie_year, api_key)
        else:
            print(f"Skipping invalid folder name format: {folder}")

def fetch_posters_for_all(parent_dir, api_key, skip_existing=True):
    """Fetches posters for all directories automatically, skipping existing covers if specified."""
    for folder in os.listdir(parent_dir):
        folder_path = os.path.join(parent_dir, folder)
        if os.path.isdir(folder_path):
            match = re.match(r"(.+) \((\d{4})\).*", folder)
            if match:
                movie_title, movie_year = match.groups()
                fetch_movie_poster(folder_path, movie_title, movie_year, api_key, skip_existing)
            else:
                print(f"Skipping invalid folder name format: {folder}")

if __name__ == '__main__':

    parent_directory = "D:\Movies"

    # Fetch posters for selected folders
    # get_movie_poster_for_selected(parent_directory, OMDB_API_KEY)

    # Fetch posters for all folders automatically (set skip_existing to False to force re-downloads)
    fetch_posters_for_all(parent_directory, OMDB_API_KEY, skip_existing=True)
