import sys
import os
from pathlib import Path
from spotdl import Spotdl


def download_tracks(urls, target_dir):
    # Retrieve secrets from environment variables
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("Spotify client ID and secret must be provided.")

    # Ensure the target directory exists
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    # Change the current working directory to the target directory
    os.chdir(target_dir)

    spotdl = Spotdl(client_id=client_id, client_secret=client_secret, headless=True)
    songs = spotdl.search(urls)
    tracks = spotdl.download_songs(songs)
    return tracks


if __name__ == "__main__":
    urls = sys.argv[1:-1]
    target_dir = sys.argv[-1]
    download_tracks(urls, target_dir)
