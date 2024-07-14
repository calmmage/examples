import subprocess
from pathlib import Path
from typing import Union


def get_audio_duration_ffmpeg(audio_path):
    """Returns audio duration in seconds using ffprobe"""
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(audio_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return float(result.stdout.strip())


def pick_optimal_segment_duration_ffmpeg(
    total_duration,
    min_segment_duration,
    max_segment_duration,
    min_num_chunks,
    max_num_chunks,
):
    # if all is None - raise
    if (
        min_segment_duration is None
        and max_segment_duration is None
        and min_num_chunks is None
        and max_num_chunks is None
    ):
        raise ValueError("At least one of the parameters should be provided")

    if min_num_chunks is not None:
        max_duration_from_chunks = total_duration / min_num_chunks
        if max_segment_duration is not None:
            max_segment_duration = min(max_segment_duration, max_duration_from_chunks)
        else:
            max_segment_duration = max_duration_from_chunks

    if max_num_chunks is not None:
        min_duration_from_chunks = total_duration / max_num_chunks
        if min_segment_duration is not None:
            min_segment_duration = max(min_segment_duration, min_duration_from_chunks)
        else:
            min_segment_duration = min_duration_from_chunks

    if min_segment_duration is not None and max_segment_duration is not None:
        if min_segment_duration > max_segment_duration:
            raise ValueError(
                f"resulting {min_segment_duration=} is greater than {max_segment_duration=}"
            )

    return min_segment_duration or max_segment_duration


Pathlike = Union[str, Path]


def split_audio_with_overlap_ffmpeg(
    audio_path,
    max_segment_duration=None,
    min_segment_duration=None,
    min_num_chunks=None,
    max_num_chunks=None,
    output_path: Pathlike = None,
    overlap_duration=5,
):
    audio_path = Path(audio_path)
    total_duration = get_audio_duration_ffmpeg(audio_path)
    segment_duration = pick_optimal_segment_duration_ffmpeg(
        total_duration,
        min_segment_duration,
        max_segment_duration,
        min_num_chunks,
        max_num_chunks,
    )

    if output_path is None:
        output_path = audio_path.parent / f"{audio_path.stem}_segments"
        output_path.mkdir(exist_ok=True)

    segment_path_template = (
        output_path / f"{audio_path.stem}_segment%03d{audio_path.suffix}"
    )
    command = [
        "ffmpeg",
        "-i",
        str(audio_path),  # Input file
        "-f",
        "segment",  # Format to use for segmenting
        "-segment_time",
        str(segment_duration),  # Duration of each segment in seconds
        "-segment_overlap",
        str(overlap_duration),  # Overlap duration in seconds
        "-c",
        "copy",  # Use the same codec
        str(segment_path_template),  # Output path pattern
    ]

    # Execute the command
    subprocess.run(command, check=True)

    return list(output_path.iterdir())


import typer
from typing import Optional

app = typer.Typer(help="Split an audio file into segments with specified overlap.")


@app.command("split")
def split_audio(
    audio_path: str = typer.Argument(..., help="Path to the audio file."),
    max_segment_duration: Optional[int] = typer.Option(
        None, help="Maximum duration of each segment in seconds."
    ),
    min_segment_duration: Optional[int] = typer.Option(
        None, help="Minimum duration of each segment in seconds."
    ),
    min_num_chunks: Optional[int] = typer.Option(
        None, help="Minimum number of chunks."
    ),
    max_num_chunks: Optional[int] = typer.Option(
        None, help="Maximum number of chunks."
    ),
    output_path: str = typer.Option(..., help="Output path for the segments."),
    overlap_duration: int = typer.Option(5, help="Overlap duration in seconds."),
):
    """
    Process an audio file by splitting it into segments, with overlap and other configurable parameters.
    """
    split_audio_with_overlap_ffmpeg(
        audio_path,
        max_segment_duration,
        min_segment_duration,
        min_num_chunks,
        max_num_chunks,
        output_path,
        overlap_duration,
    )


if __name__ == "__main__":
    app()
#
# if __name__ == "__main__":
#     import argparse
#
#     parser = argparse.ArgumentParser(
#         description="Split audio file into segments with overlap"
#     )
#
#     parser.add_argument("audio_path", type=str, help="Path to the audio file")
#     parser.add_argument(
#         "--max_segment_duration",
#         type=int,
#         help="Maximum duration of each segment in seconds",
#     )
#     parser.add_argument(
#         "--min_segment_duration",
#         type=int,
#         help="Minimum duration of each segment in seconds",
#     )
#     parser.add_argument(
#         "--min_num_chunks",
#         type=int,
#         help="Minimum number of chunks",
#     )
#     parser.add_argument(
#         "--max_num_chunks",
#         type=int,
#         help="Maximum number of chunks",
#     )
#     parser.add_argument(
#         "--output_path",
#         type=str,
#         help="Output path for the segments",
#     )
#     parser.add_argument(
#         "--overlap_duration",
#         type=int,
#         default=5,
#         help="Overlap duration in seconds",
#     )
#
#     args = parser.parse_args()
#
#     split_audio_with_overlap_ffmpeg(
#         args.audio_path,
#         args.max_segment_duration,
#         args.min_segment_duration,
#         args.min_num_chunks,
#         args.max_num_chunks,
#         args.output_path,
#         args.overlap_duration,
#     )
