"""
Converts video to audio using moviepy library

In-place, with limited memory usage
"""

from pathlib import Path
from typing import Union, Optional

from moviepy.editor import VideoFileClip

Pathlike = Union[str, Path]


def convert_video_to_audio(
    video_path: Pathlike, output_audio_path: Optional[Pathlike] = None
):
    video_path = Path(video_path)
    # Load the video file
    video_clip = VideoFileClip(str(video_path))

    # Extract audio from the video
    audio_clip = video_clip.audio

    # Define the new audio file path (same as video but with .mp3 extension)
    if output_audio_path is None:
        output_audio_path = video_path.with_suffix(".mp3")

    # Write the audio file to disk
    audio_clip.write_audiofile(output_audio_path)

    # Close the clips
    video_clip.close()
    audio_clip.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert video to audio")
    parser.add_argument("video_path", type=str, help="Path to the video file")
    parser.add_argument(
        "output_audio_path",
        type=str,
        help="Path to the output audio file (default: video_path with .mp3 extension)",
        nargs="?",
    )

    args = parser.parse_args()

    convert_video_to_audio(args.video_path, args.output_audio_path)
