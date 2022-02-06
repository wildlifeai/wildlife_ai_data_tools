"""This module allows naive processing of videos."""
import itertools
import os
import shutil

import click
import cv2
import numpy as np


# taken from itertools recipes(exists in 3.10+)
def pairwise(iterable):
    """Creates all tuples that contain an item with its adjacent items.

    Example: s -> (s0,s1), (s1,s2), (s2, s3), ...

    Args:
        iterable: any type of iterable

    Returns:
        generator of the tuples
    """
    op1, op2 = itertools.tee(iterable)
    next(op2, None)
    return zip(op1, op2)


def convert_video_to_frames(src_file):
    """Get a video and returns frames.

    Args:
        src_file: full path filename

    Returns:
        list of all frames from the video
    """
    # reader = iio.get_reader(src_file, 'ffmpeg')
    reader = cv2.VideoCapture(src_file)
    frames = []
    success = True
    while success:
        success, frame = reader.read()
        frames.append(frame)
    return frames


def check_frames_differences(frames):
    """Return a list of differences between 2 adjacent frames.

    Args:
        frames: List of frames

    Returns:
        List of differences between any two adjacent frames
    """
    # Ideally this is where a new model would allow to distinguish
    diffs = []
    for frame1, frame2 in pairwise(frames):
        if frame2 is None:
            diff = 0
        else:
            diff = np.sum(
                cv2.absdiff(frame1, frame2) >= 50
            )  # this gave me surprisingly good results so far
        diffs.append(diff)
    return diffs


def video_process_content(src_file):
    """Check content of the video and returns if the video is empty.

    Args:
        src_file: full path filename

    Returns:
        True if video is empty. Otherwise, False.
    """
    frames = convert_video_to_frames(src_file)
    frame_diff = check_frames_differences(frames)
    if any(x > 0 for x in frame_diff):
        return False

    return True


@click.command()
@click.option("--src", default=".", type=click.Path(exists=True))
@click.option("--dest", default="empty_videos", type=click.Path())
@click.option("--dry-run", is_flag=True)
def cli(src, dest, dry_run):
    """Move all empty videos to a folder specified by the user.

    Args:
        src: Path that must already exist with the videos to process
        dest: Path, where to dump the files
        dry_run: boolean
    """
    os.makedirs(dest, exist_ok=True)

    for src_file in os.listdir(src):
        full_src_file = os.path.abspath(os.path.join(src, src_file))
        if not src_file.endswith(".mjpg"):
            click.echo(f"Found a non video file named: {src_file}")
            continue

        click.echo(f"Processing file {src_file} ...")
        is_empty = video_process_content(full_src_file)
        if is_empty:
            click.echo(f"Moving {full_src_file} to {dest}{src_file}")
            if not dry_run:
                shutil.move(full_src_file, os.path.join(dest, src_file))


if __name__ == "__main__":
    cli()
