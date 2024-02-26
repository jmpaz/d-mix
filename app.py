import os
import gradio as gr
from d_mix.download import download_tracks
from d_mix.demucs import DemucsClient


def init():
    def read_secrets(filename="secrets.txt"):
        secrets = {}
        with open(filename, "r") as file:
            for line in file:
                key, value = line.strip().split("=", 1)
                secrets[key] = value
        return secrets

    if "SPOTIFY_CLIENT_ID" not in os.environ:
        secrets = read_secrets()
        os.environ["SPOTIFY_CLIENT_ID"] = secrets["client_id"]
        os.environ["SPOTIFY_CLIENT_SECRET"] = secrets["client_secret"]


def process(url):
    download_result = download_tracks([url], target_dir=".tmp")
    track_path = f".tmp/{download_result[0][1]}"
    print(f"Downloaded {track_path}")

    print(os.getcwd())
    client = DemucsClient([track_path])
    output_paths = client.separate()
    print(f"Separated into {output_paths}")

    return output_paths


with gr.Blocks(
    title="d-mix",
    css="footer {visibility: hidden}",
) as app:
    name = gr.Markdown("# d-mix")

    with gr.Row():
        with gr.Column(elem_id="inputs", variant="panel"):
            gr.Markdown(
                "_Paste a Spotify URL and click 'Start' to download song and prepare stems._"
            )

            with gr.Row():
                url = gr.Textbox(
                    label="URL",
                    placeholder="https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT",
                    lines=2,
                    scale=6,
                )
                start_btn = gr.Button(value="Start", scale=1)

        with gr.Column(elem_id="output", visible=True):
            files = gr.Files(
                label="Output",
            )

    url.submit(fn=process, inputs=[url], outputs=[files])
    start_btn.click(fn=process, inputs=[url], outputs=[files])


init()
app.launch(server_name="0.0.0.0", server_port=7862)
