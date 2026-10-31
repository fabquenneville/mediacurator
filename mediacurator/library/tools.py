#!/usr/bin/env python3
"""
These are various tools used by mediacurator
"""

import argparse
import argcomplete
import re
import shutil
import subprocess
import os
import sys
from functools import lru_cache

# Import colorama for colored output
import colorama

colorama.init()

# Define color codes for colored output
cblue = colorama.Fore.BLUE
cgreen = colorama.Fore.GREEN
cred = colorama.Fore.RED
cyellow = colorama.Fore.YELLOW
creset = colorama.Fore.RESET


def load_arguments():
    """Get/load command parameters

    Returns:
        Namespace: An argparse.Namespace object containing options passed by the user
    """
    parser = argparse.ArgumentParser(description="mediacurator CLI Tool")

    # Add a positional argument for the command
    parser.add_argument(
        "command",
        choices=["list", "test", "convert"],
        help="Command to run",
    )

    # Add other arguments with both short and long options, including defaults
    parser.add_argument(
        "-del",
        "--delete",
        action="store_true",
        help="Delete found results after successful operations",
    )

    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="skip confirmation prompts",
    )

    parser.add_argument(
        "-i",
        "--inputs",
        type=str,
        nargs="*",
        default=["any"],
        help="Input options (default: any)",
    )

    parser.add_argument(
        "-fl",
        "--filters",
        type=str,
        nargs="*",
        default=[],
        help="Filters to apply",
    )

    parser.add_argument(
        "-o",
        "--outputs",
        type=str,
        nargs="*",
        default=["mkv", "x265"],
        help="Output options (default: mkv, x265)",
    )

    parser.add_argument(
        "-p",
        "--printop",
        type=str,
        nargs="*",
        default=["list"],
        help="Print options (default: list)",
    )

    parser.add_argument(
        "-f",
        "--files",
        type=str,
        nargs="*",
        default=[],
        help="Files to process",
    )

    parser.add_argument(
        "-d",
        "--dirs",
        type=str,
        nargs="*",
        default=[],
        help="Directories to process",
    )

    # Activate argcomplete
    argcomplete.autocomplete(parser)

    args = parser.parse_args()

    # Confirm with the user about deletion if delete option is selected
    if args.delete:
        print(f"{cyellow}WARNING: Delete option selected!{creset}")
        if not args.yes and not user_confirm(
            "Are you sure you wish to delete all found results after selected operations are successful? [Y/N] ?",
            color="yellow",
        ):
            print(f"{cgreen}Exiting!{creset}")
            sys.exit()

    return args


def detect_ffmpeg():
    """Returns the version of ffmpeg that is installed or False

    Returns:
        str: The version number of the installed FFMPEG
        False: If version retrieval failed
    """
    try:
        txt = subprocess.check_output(
            ["ffmpeg", "-version"], stderr=subprocess.STDOUT
        ).decode()
        if "ffmpeg version" in txt:
            # Strip the useless text
            return txt.split(" ")[2]
    except (OSError, subprocess.CalledProcessError):
        pass
    return False


def check_ffmpeg():
    """
    Checks if ffmpeg is installed and returns its version.

    Returns:
        str: ffmpeg version or None if not detected
    """
    ffmpeg_version = detect_ffmpeg()
    if not ffmpeg_version:
        print(f"{cred}No ffmpeg version detected{creset}")
        sys.exit(1)
    if shutil.which("ffprobe") is None:
        print(f"{cred}No ffprobe detected{creset}")
        sys.exit(1)
    print(f"{cblue}ffmpeg version detected: {ffmpeg_version}{creset}")
    return ffmpeg_version


def user_confirm(question, color=False):
    """Returns the user's answer to a yes or no question

    Args:
        question (str): The user question
        color (str, optional): The preferred color for a question (red/yellow)
    Returns:
        bool: True for a positive response, False otherwise
    """
    if color == "yellow":
        print(f"{cyellow}{question} {creset}", end="")
        answer = input()
    elif color == "red":
        print(f"{cred}{question} {creset}", end="")
        answer = input()
    else:
        answer = input(f"{question} ")
    if answer.lower() in ["y", "yes"]:
        return True
    elif answer.lower() in ["n", "no"]:
        return False
    print("Please answer with yes (Y) or no (N)...")
    return user_confirm(question, color=color)


def deletefile(filepath):
    """Delete a file and return a boolean indicating success

    Args:
        filepath (str): The full filepath
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.remove(filepath)
    except OSError:
        print(f"{cred}Error deleting {filepath}{creset}")
        return False

    print(f"{cgreen}Successfully deleted {filepath}{creset}")
    return True


def findfreename(filepath, tag="HEVC"):
    """Find a free filename by appending [tag] or [tag](#) to the name if necessary

    Args:
        filepath (str): The full filepath
        tag (str, optional): The label to add, e.g. HEVC, AV1 or AV2
    Returns:
        str: The first free filepath found
    """
    if not os.path.exists(filepath):
        return filepath

    root, extension = os.path.splitext(str(filepath))
    candidate = f"{root}[{tag}]{extension}"
    attempt = 0
    while os.path.exists(candidate):
        attempt += 1
        candidate = f"{root}[{tag}]({attempt}){extension}"
    return candidate


@lru_cache(maxsize=None)
def find_encoder(codec):
    """Find an ffmpeg encoder for a codec by asking the installed ffmpeg.

    Nothing is hardcoded, so this keeps working whatever name an encoder
    ends up with (e.g. libaom-av1 and libsvtav1 both report "(codec av1)").

    Args:
        codec (str): The codec name, e.g. "av2"
    Returns:
        str: The name of the first matching encoder, or None if there is none
    """
    try:
        output = subprocess.check_output(
            ["ffmpeg", "-hide_banner", "-encoders"], stderr=subprocess.STDOUT
        ).decode(errors="replace")
    except (OSError, subprocess.CalledProcessError):
        return None

    for line in output.splitlines():
        match = re.match(r"^\s*V\S*\s+(\S+)\s+(.*)$", line)
        if not match:
            continue
        name, rest = match.groups()
        tag = re.search(r"\(codec (\S+?)\)", rest)
        if name == codec or (tag and tag.group(1) == codec):
            return name
    return None
