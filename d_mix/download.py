import sys
import os
from pathlib import Path
from spotdl import Spotdl


def get_spotdl_client(client_id, client_secret):
    if "spotdl_client" not in globals():
        globals()["spotdl_client"] = Spotdl(
            client_id=client_id, client_secret=client_secret, headless=True
        )

    return globals()["spotdl_client"]


def download_tracks(urls, target_dir=".tmp"):
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("Spotify client ID and secret must be provided.")

    # Create and enter the target directory
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    os.chdir(target_dir)

    spotdl = get_spotdl_client(client_id, client_secret)
    songs = spotdl.search(urls)
    tracks = spotdl.download_songs(songs)
    os.chdir("..")
    return tracks


if __name__ == "__main__":
    urls = sys.argv[1:-1]
    target_dir = sys.argv[-1]
    download_tracks(urls, target_dir)
