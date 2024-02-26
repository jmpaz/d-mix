import os
import demucs.api


class DemucsClient:
    def __init__(self, base_tracks, stems=None):
        self.base_tracks = base_tracks
        self.stems = stems
        self.separator = demucs.api.Separator()

    def separate(self):
        output_paths = []

        for track_path in self.base_tracks:
            print(f"Processing {track_path}")

            # Extract track stems
            origin, stems = self.separator.separate_audio_file(track_path)
            vocals = stems["vocals"]
            no_vocals = origin - vocals

            # Get the original file extension and construct the output directory
            _, file_extension = os.path.splitext(track_path)
            track_dir = (
                f"outputs/{track_path.split('/')[-1].replace(file_extension, '')}"
            )
            os.makedirs(track_dir, exist_ok=True)

            for stem, source in stems.items():
                print(f"Saving '{stem}'")
                output_path = f"{track_dir}/{stem}{file_extension}"
                demucs.api.save_audio(
                    source, output_path, samplerate=self.separator.samplerate
                )
                output_paths.append(output_path)

            print("Saving 'no_vocals'")
            no_vocals_path = f"{track_dir}/all, minus vocals{file_extension}"
            demucs.api.save_audio(
                no_vocals, no_vocals_path, samplerate=self.separator.samplerate
            )
            output_paths = [no_vocals_path] + output_paths

        print("Separation completed.")
        return output_paths
