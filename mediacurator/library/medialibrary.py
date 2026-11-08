#!/usr/bin/env python3
"""This module defines the MediaLibrary class, which manages information about the workspace and all videos in it."""

import os
import re

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .video import Video
from .tools import deletefile

# Import colorama for colored output
import colorama

colorama.init()

# Define color codes for colored output
ccyan = colorama.Fore.CYAN
cgreen = colorama.Fore.GREEN
cred = colorama.Fore.RED
cyellow = colorama.Fore.YELLOW
creset = colorama.Fore.RESET

# Constants
VIDEO_EXTENSIONS = frozenset(
    {
        "3g2",
        "3gp",
        "amv",
        "asf",
        "avi",
        "dav",
        "divx",
        "dv",
        "f4v",
        "flv",
        "gif",
        "m1v",
        "m2p",
        "m2t",
        "m2ts",
        "m2v",
        "m4p",
        "m4v",
        "mkv",
        "mov",
        "mp4",
        "mpe",
        "mpeg",
        "mpg",
        "mpv",
        "mts",
        "mxf",
        "ogm",
        "ogv",
        "qt",
        "rm",
        "rmvb",
        "swf",
        "tod",
        "ts",
        "vid",
        "vob",
        "webm",
        "wm",
        "wmv",
        "wtv",
    }
)
PROBE_WORKERS = min(8, os.cpu_count() or 4)
MODERN_CODECS = frozenset({"hevc", "av1", "av2"})
CODEC_FILTERS = {
    "mpeg4": {"mpeg4", "msmpeg4v3"},
    "mpeg": {"mpeg4", "msmpeg4v3", "mpeg1video"},
    "wmv3": {"wmv3"},
    "wmv": {"wmv3"},
    "h264": {"h264"},
    "hevc": {"hevc"},
    "x265": {"hevc"},
    "av1": {"av1"},
    "av2": {"av2"},
}
DEFINITION_FILTERS = {
    "subsd": {"subsd"},
    "sd": {"sd"},
    "720p": {"720p"},
    "1080p": {"1080p"},
    "2160p": {"uhd"},
    "uhd": {"uhd"},
    "4k": {"uhd"},
    "lowres": {"subsd", "sd"},
    "hd": {"720p", "1080p", "uhd"},
}
VALID_FILTERS = (
    frozenset(CODEC_FILTERS) | frozenset(DEFINITION_FILTERS) | {"old", "fferror"}
)


def human_size(size):
    """Formats a size in bytes as MB, or KB for files under 1 MB."""
    if size >= 1024 * 1024:
        return f"{size / 1024 / 1024:.1f} MB"
    return f"{size / 1024:.0f} KB"


def error_lines(error):
    """Normalizes ffprobe error output into a set of comparable lines.

    Memory addresses like '0x55e7252ae4c0' change on every run, so they are
    masked: the same underlying problem then compares equal across two files.
    """
    if not error:
        return set()
    return {
        re.sub(r"0x[0-9a-f]+", "0x?", line.strip())
        for line in str(error).splitlines()
        if line.strip()
    }


def is_old_codec(codec):
    """True for a known, non-modern codec. Unknown or undetected codecs are NOT
    old: ffprobe can't name a codec it doesn't support (e.g. a brand new one),
    and such files must not be swept up by '--filters old --delete'."""
    return bool(codec) and codec != "unknown" and codec not in MODERN_CODECS


class MediaLibrary:
    """This class manages information about the workspace and all videos in it."""

    def __init__(
        self, files=None, directories=None, inputs=None, filters=None, verbose=False
    ):
        """
        Initializes a MediaLibrary instance with provided parameters.

        Args:
            files (list or None): A list of video files to load into the library.
            directories (list or None): A list of directories containing videos directly or in subdirectories.
            inputs (list or None): Extensions to include when browsing directories (default is ["any"]).
            filters (list or None): A list of filters to apply to the videos (default is none).
            verbose (bool): A flag to enable verbose output (default is False).
        """

        self.directories = None
        self.inputs = inputs or ["any"]
        self.filters = [f.lower() for f in (filters or [])]
        self.videos = dict()

        unknown = sorted(set(self.filters) - VALID_FILTERS)
        if unknown:
            raise ValueError(
                f"Unknown filter(s): {', '.join(unknown)}. "
                f"Valid filters: {', '.join(sorted(VALID_FILTERS))}"
            )

        # Load files if provided
        if files:
            self.load_files(files, verbose)

        # Load directories if provided
        elif directories:
            self.directories = directories
            self.load_directories(verbose)

        else:
            raise ValueError("No files or directories provided.")

        # Filter the loaded videos based on the specified filters
        self.filter_videos(verbose)

    def __str__(self):
        """
        Returns a string representation of the MediaLibrary instance.

        Returns:
            str: Information about the MediaLibrary instance.
        """

        text = ""
        if self.directories:
            text += f"mediacurator is watching the following directories: \n"
            text += "\n    ".join(map(str, self.directories)) + "\n"
        text += f"mediacurator is tracking {len(self.videos)} video files"
        return text

    def load_files(self, files, verbose=False):
        for filepath in files:
            self.videos[filepath] = Video(filepath, verbose=verbose)

    def load_directories(self, verbose=False):
        """
        Scans folders for video files respecting the inputs requested by the user
        and saves them to the videos dictionary.

        Args:
            verbose (bool): A flag to enable verbose output.
        """

        print(
            f"{cgreen}Scanning files in {', '.join(map(str, self.directories))} for videos{creset}"
        )

        # Decide once which extensions to accept
        if not self.inputs or "any" in self.inputs:
            wanted = VIDEO_EXTENSIONS
        else:
            wanted = VIDEO_EXTENSIONS & {i.lower() for i in self.inputs}

        videolist = []

        for directory in self.directories:
            for root, _dirs, files in os.walk(directory):
                for name in files:
                    ext = os.path.splitext(name)[1][1:].lower()
                    if ext in wanted:
                        videolist.append(Path(root) / name)

        # Map it all to the videos dictionary as initiated Video objects
        print(
            f"{cgreen}Analyzing {len(videolist)} videos in {', '.join(map(str, self.directories))}{creset}"
        )

        total = len(videolist)
        with ThreadPoolExecutor(max_workers=PROBE_WORKERS) as executor:
            results = executor.map(lambda path: Video(path, verbose=verbose), videolist)
            for i, (path, video) in enumerate(zip(videolist, results), 1):
                if verbose:
                    print(f"{int(i / total * 100)}% complete", end="\r")
                self.videos[path] = video

    def filter_videos(self, verbose=False):
        """
        Marks videos for operation in the videos dictionary (default is not to operate).

        Filters of different kinds (codec, resolution, fferror) are combined with AND,
        filters of the same kind with OR.

        Args:
            verbose (bool): A flag to enable verbose output.
        """

        print(
            f"{cgreen}Filtering {len(self.videos)} videos for the requested parameters{creset}"
        )

        codec_filters = [f for f in self.filters if f in CODEC_FILTERS or f == "old"]
        definitions = set()
        for f in self.filters:
            definitions |= DEFINITION_FILTERS.get(f, set())
        resolution_requested = any(f in DEFINITION_FILTERS for f in self.filters)

        for video in self.videos.values():
            if codec_filters:
                video.operate = any(
                    is_old_codec(video.codec)
                    if f == "old"
                    else video.codec in CODEC_FILTERS[f]
                    for f in codec_filters
                )

            if video.operate and resolution_requested:
                video.operate = video.definition in definitions

            if video.operate and "fferror" in self.filters:
                video.operate = bool(video.error)

        found = sum(1 for video in self.videos.values() if video.operate)
        print(f"{cgreen}Found {found} videos for the requested parameters{creset}")

    def unwatch(self, filepath, delete=False):
        """
        Removes a video from the index and deletes it if requested.

        Args:
            filepath (str): The full filepath of the video.
            delete (bool): If True, delete the file as well as removing it from the library.

        Returns:
            bool: True if operation successful, False otherwise.
        """

        if delete:
            deletefile(filepath)
        try:
            video = self.videos.pop(filepath)
            if video:
                return video
        except KeyError:
            pass
        return False

    def list_videos(self, formatted: bool = False, delete: bool = False):
        # Create a sorted list of videos marked for operation
        keylist = sorted(
            filepath for filepath in self.videos if self.videos[filepath].operate
        )

        for filepath in keylist:
            self.videos[filepath].print_details(formatted)

            # If deletion is requested, delete and unwatch the video
            if delete:
                self.unwatch(filepath, delete=True)

    def test_videos(self, formatted: bool = False, delete: bool = False):
        # For testing, we can just call the list_videos method as they behave similarly
        self.list_videos(formatted, delete)

    def convert_videos(
        self,
        vcodec: str,
        formatted: bool = False,
        verbose: bool = False,
        delete: bool = False,
        delete_on_reduce: bool = False,
        preset=None,
        crf=None,
    ):
        counter = 0

        # Create a sorted list of videos marked for operation
        keylist = sorted(
            filepath for filepath in self.videos if self.videos[filepath].operate
        )

        for filepath in keylist:
            counter += 1

            # Print conversion start information
            print(
                f"{cgreen}\n******  Starting conversion {counter} of {len(keylist)}: '{ccyan}{self.videos[filepath].filename_origin}{cgreen}' from {ccyan}{self.videos[filepath].codec}{cgreen} to {ccyan}{vcodec}{cgreen}...{creset}"
            )
            print(f"{ccyan}Original file:{creset}")

            self.videos[filepath].print_details(formatted)

            print(f"{cgreen}Converting, please wait...{creset}", end="\r")

            # Perform the conversion
            if self.videos[filepath].convert(
                vcodec, verbose=verbose, preset=preset, crf=crf
            ):
                # Mark video as processed
                self.videos[filepath].operate = False

                # Get the path for the new video file
                newfpath = (
                    self.videos[filepath].path + self.videos[filepath].filename_new
                )

                # Add the new video to the library
                self.videos[newfpath] = Video(newfpath, operate=False, verbose=verbose)

                # Print success message with details about the conversion
                print(
                    f"{cgreen}Successfully converted '{self.videos[filepath].filename_origin}'{ccyan}({self.videos[filepath].filesize}mb){cgreen} to '{self.videos[newfpath].filename_origin}'{ccyan}({self.videos[newfpath].filesize}mb){cgreen}, {ccyan}new file:{creset}"
                )

                # Display detailed information about the new video
                self.videos[newfpath].print_details(formatted)

                # If deletion is requested, delete the original, but only once the
                # new file has been read back without new errors
                if delete or delete_on_reduce:
                    original = self.videos[filepath]
                    newvideo = self.videos[newfpath]
                    introduced = error_lines(newvideo.error) - error_lines(
                        original.error
                    )

                    sizes = None
                    if delete_on_reduce:
                        try:
                            sizes = (
                                os.path.getsize(filepath),
                                os.path.getsize(newfpath),
                            )
                        except OSError:
                            pass

                    if introduced or not newvideo.codec:
                        print(
                            f"{cred}\nKeeping the original: the new file failed verification{creset}"
                        )
                        for line in sorted(introduced):
                            print(f"{cred}    {line}{creset}")
                    elif delete_on_reduce and (sizes is None or sizes[1] >= sizes[0]):
                        detail = (
                            "could not compare file sizes"
                            if sizes is None
                            else f"{human_size(sizes[1])} vs {human_size(sizes[0])}"
                        )
                        print(
                            f"{cyellow}Keeping the original: the new file is not smaller ({detail}){creset}"
                        )
                    else:
                        self.unwatch(filepath, delete=True)
