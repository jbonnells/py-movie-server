import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')


def list_movie_folders(parent_dir):
    """Lists all movie directories numerically and returns a mapping of numbers to folder names."""
    movie_folders = [f for f in os.listdir(parent_dir)
                     if os.path.isdir(os.path.join(parent_dir, f))]

    if not movie_folders:
        print("No movie folders found.")
        return {}

    folder_map = {}
    print("Select a movie folder by number:")
    for idx, folder in enumerate(movie_folders, 1):
        print(f"{idx}: {folder}")
        folder_map[str(idx)] = folder

    return folder_map


def list_folders_missing_cover(parent_dir):
    """Lists directories missing cover.jpg or cover.png and returns a mapping of numbers to folder names."""
    missing = []
    for folder in os.listdir(parent_dir):
        path = os.path.join(parent_dir, folder)
        if os.path.isdir(path):
            has_jpg = os.path.exists(os.path.join(path, "cover.jpg"))
            has_png = os.path.exists(os.path.join(path, "cover.png"))
            if not (has_jpg or has_png):
                missing.append(folder)

    if not missing:
        print("All folders have a cover image.")
        return {}

    folder_map = {}
    print("Folders missing cover image:")
    for idx, folder in enumerate(missing, 1):
        print(f"{idx}: {folder}")
        folder_map[str(idx)] = folder

    return folder_map


def fetch_movie_poster(folder_path, movie_title, movie_year, api_key,
                       skip_existing=True):
    """Fetches and saves a movie poster to the given directory."""
    # Accept both .jpg and .png as valid existing covers
    file_jpg = os.path.join(folder_path, "cover.jpg")
    file_png = os.path.join(folder_path, "cover.png")
    if skip_existing and (os.path.exists(file_jpg) or os.path.exists(file_png)):
        return

    print(f"Fetching poster for: {movie_title} ({movie_year or 'Year N/A'})")
    params = {'apikey': api_key, 't': movie_title}
    if movie_year:
        params['y'] = movie_year

    response = requests.get("http://www.omdbapi.com/", params=params).json()
    if response.get("Response") != "True":
        print(f"Movie not found: {movie_title} ({movie_year})")
        return

    poster_url = response.get("Poster")
    if not poster_url or poster_url == "N/A":
        print(f"Poster not available for: {movie_title} ({movie_year})")
        return

    img_data = requests.get(poster_url).content
    ext = ".jpg" if poster_url.lower().endswith('.jpg') else ".png"
    file_path = os.path.join(folder_path, f"cover{ext}")
    with open(file_path, 'wb') as img_file:
        img_file.write(img_data)
    print(f"Saved poster: {file_path}")


def get_movie_poster_for_selected(parent_dir, api_key):
    """Interactive selection of folders to fetch posters for."""
    folder_map = list_movie_folders(parent_dir)
    if not folder_map:
        return

    choices = input("Enter numbers of folders to fetch (comma-separated): ").split(',')
    selections = [c.strip() for c in choices if c.strip() in folder_map]
    if not selections:
        print("No valid selections.")
        return

    for choice in selections:
        folder = folder_map[choice]
        path = os.path.join(parent_dir, folder)
        match = re.match(r"(.+) \((\d{4})\)", folder)
        if match:
            title, year = match.groups()
            fetch_movie_poster(path, title, year, api_key)
        else:
            print(f"Skipping: invalid folder name '{folder}'")


def manual_fetch_movie_poster(api_key):
    """Allows manual input of a movie title/year and destination to save poster."""
    title = input("Enter movie title: ").strip()
    year = input("Enter movie year (optional): ").strip() or None
    destination = input("Enter folder path to save poster: ").strip()
    if not os.path.isdir(destination):
        print("Destination not a valid directory.")
        return
    fetch_movie_poster(destination, title, year, api_key, skip_existing=False)


def fetch_posters_for_all(parent_dir, api_key, skip_existing=True):
    """Fetch posters for every valid movie folder."""
    for folder in os.listdir(parent_dir):
        path = os.path.join(parent_dir, folder)
        if not os.path.isdir(path):
            continue
        match = re.match(r"(.+) \((\d{4})\)", folder)
        if match:
            title, year = match.groups()
            fetch_movie_poster(path, title, year, api_key, skip_existing)
        else:
            print(f"Skipping folder: '{folder}'")


if __name__ == '__main__':
    parent_directory = r"D:\Movies"

    while True:
        print("\nMenu: 1) All posters  2) Select folders  3) Manual fetch  4) List missing covers  5) Exit")
        choice = input("Choose option: ").strip()
        if choice == '1':
            fetch_posters_for_all(parent_directory, OMDB_API_KEY)
        elif choice == '2':
            get_movie_poster_for_selected(parent_directory, OMDB_API_KEY)
        elif choice == '3':
            manual_fetch_movie_poster(OMDB_API_KEY)
        elif choice == '4':
            list_folders_missing_cover(parent_directory)
        elif choice == '5':
            break
        else:
            print("Invalid option.")
