#!/usr/bin/env python3
"""This module defines the Video class, which contains information and methods for video files."""

from .tools import deletefile, findfreename, find_encoder
import shutil
import subprocess
import os
import sys

# Import colorama for colored output
import colorama

colorama.init()

# Define color codes for colored output
cyellow = colorama.Fore.YELLOW
cred = colorama.Fore.RED
creset = colorama.Fore.RESET

# Constants
AV2_QUALITY_ARGS = ["-crf", "30"]


class Video:
    """Contains the information and methods of a video file."""

    def __init__(self, filepath, operate=True, verbose=False):
        """Initializes a Video instance with provided parameters.

        Args:
            filepath (str): The full filepath of the video.
            operate (bool): A flag indicating if the video is to be operated on.
            verbose (bool): A flag indicating whether to enable verbose output.
        """

        # Initialize attributes
        self.path = None
        self.filename_origin = None
        self.filesize = None
        self.filename_new = None
        self.filename_tmp = None
        self.operate = None
        self.codec = None
        self.error = None
        self.definition = None
        self.width = None
        self.height = None

        # Break down the full path into its components
        # (self.path keeps its trailing separator, and is "" for a bare filename)
        head, self.filename_origin = os.path.split(str(filepath))
        self.path = os.path.join(head, "") if head else ""

        if not os.path.exists(filepath):
            self.error = (
                f"FileNotFoundError: [Errno 2] No such file or directory: '{filepath}'"
            )
            self.operate = operate
        else:
            # Mark the video for operation if specified manually by the user
            self.operate = operate

            # Gather information on the video
            self.filesize = self.detect_filesize(filepath)
            self.error = self.detect_fferror(filepath)
            self.codec = self.detect_codec(filepath)
            try:
                self.width, self.height = self.detect_resolution(filepath)
                self.definition = self.detect_definition(
                    width=self.width, height=self.height
                )
            except:
                self.width, self.height = False, False
                self.definition = False

        if self.error and verbose:
            print(f'{cred}There seems to be an error with "{filepath}"{creset}')
            print(f"{cred}    {self.error}{creset}")

    def __str__(self):
        """Returns a short formatted string about the video.

        Returns:
            str: A short formatted string about the video.
        """

        if type(self.error) is str and "FileNotFoundError" in self.error:
            return self.error

        text = f"{self.codec} - "

        # If the first character of the definition is not a number (e.g., UHD and not 720p), upper it
        if (
            self.definition
            and self.definition[0]
            and not self.definition[0].isnumeric()
        ):
            text += f"{self.definition.upper()}: ({self.width}x{self.height}) - "
        else:
            text += f"{self.definition}: ({self.width}x{self.height}) - "

        # Return the size in MB or GB if more than 1024 MB
        if self.filesize >= 1024:
            text += f"{self.filesize / 1024:.2f} GB - "
        else:
            text += f"{self.filesize} MB - "

        text += f"'{self.path + self.filename_origin}'"

        if self.error:
            text += f"{cred}\nErrors:{creset}"
            for err in self.error.splitlines():
                text += f"{cred}\n    {err}{creset}"

        return text

    __repr__ = __str__

    def fprint(self):
        """Returns a long formatted string about the video.

        Returns:
            str: A long formatted string about the video.
        """

        if type(self.error) is str and "FileNotFoundError" in self.error:
            return self.error

        text = f"{self.path + self.filename_origin}\n"

        if (
            self.definition
            and self.definition[0]
            and not self.definition[0].isnumeric()
        ):
            text += f"    Definition:     {self.definition.upper()}: ({self.width}x{self.height})\n"
        else:
            text += (
                f"    Definition:     {self.definition}: ({self.width}x{self.height})\n"
            )

        text += f"    Codec:          {self.codec}\n"

        # Return the size in MB or GB if more than 1024 MB
        if self.filesize >= 1024:
            text += f"    Size:           {self.filesize / 1024:.2f} GB"
        else:
            text += f"    Size:           {self.filesize} MB"

        if self.error:
            text += f"{cred}\n    Errors:{creset}"
            for err in self.error.splitlines():
                text += f"{cred}\n        {err}{creset}"

        return text

    def print_details(self, formatted=False):
        """Prints the video details, checking for errors and formatting.

        Args:
            formatted (bool): Whether to print in a formatted or unformatted style.
        """
        if self.error:
            # Print error details in red if the video has an error
            output = f"{cred}{self.fprint() if formatted else self}{creset}"
        else:
            # Print regular video details
            output = self.fprint() if formatted else str(self)

        print(output)

    def _discard_partial_output(self):
        """Removes the half-written output file after a failed or cancelled conversion."""
        partial = self.path + self.filename_tmp
        if os.path.exists(partial):
            deletefile(partial)
        self.filename_tmp = ""

    def convert(
        self,
        vcodec="x265",
        acodec=False,
        extension="mkv",
        verbose=False,
    ):
        """
        Converts the original file to the requested format / codec,
        ensuring even width/height by adding a black pixel gap if necessary.

        Args:
            vcodec (str): The new video codec, supports av2, av1 or x265.
            acodec (bool): Currently not enabled, will be for audio codecs.
            extension (str): The new video container format and file extension.
            verbose (bool): A flag enabling verbosity.

        Returns:
            bool: True if operation successful, False otherwise.
        """

        # Resolve the encoder first, so we fail before touching any file
        av2_encoder = None
        if vcodec == "av2":
            av2_encoder = find_encoder("av2")
            if not av2_encoder:
                print(
                    f"{cred}No AV2 encoder found in this ffmpeg build, "
                    f"cannot convert '{self.filename_origin}'{creset}"
                )
                return False
        elif vcodec not in ("av1", "x265", "hevc"):
            raise ValueError(f"Unsupported video codec: {vcodec}")

        tag = {"av1": "AV1", "av2": "AV2"}.get(vcodec, "HEVC")

        # Setting new filename
        base_filename, _ = os.path.splitext(self.filename_origin)
        newfilename = base_filename + (".mp4" if "mp4" in extension else ".mkv")

        if os.path.exists(self.path + newfilename):
            newfilename = os.path.basename(findfreename(self.path + newfilename, tag))

        self.filename_tmp = newfilename

        # Setting ffmpeg command
        args = [
            "ffmpeg",
            "-i",
            self.path + self.filename_origin,
            "-map",
            "0:v",
            "-map",
            "0:a?",
            "-map",
            "0:s?",
            "-map_metadata",
            "0",
        ]

        # Conversion options based on codec
        if vcodec == "av1":
            args += ["-c:v", "libsvtav1", "-preset", "6", "-crf", "30"]
        elif vcodec == "av2":
            args += ["-c:v", av2_encoder] + AV2_QUALITY_ARGS
        else:
            args += ["-c:v", "libx265"]
            # Control quality with crf for x265
            args += ["-preset", "medium", "-crf", "28"]
            # Add max_muxing_queue_size to avoid buffer overflows
            args += ["-max_muxing_queue_size", "1000"]

        # Encoders need even width/height: pad with a black pixel if needed
        if self.width and self.height:
            width_canvas = self.width + self.width % 2
            height_canvas = self.height + self.height % 2
            if (width_canvas, height_canvas) != (self.width, self.height):
                args += [
                    "-vf",
                    f"pad={width_canvas}:{height_canvas}:(ow-iw)/2:(oh-ih)/2:black",
                ]

        # Copy audio and subtitles without re-encoding
        args += ["-c:a", "copy", "-c:s", "copy"]

        # Specify output file
        args += [self.path + self.filename_tmp]

        try:
            if verbose:
                subprocess.run(args, check=True)
            else:
                subprocess.check_output(args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            self._discard_partial_output()
            print(f"{cred}Conversion failed {e}{creset}")
            return False
        except KeyboardInterrupt:
            print(f"{cyellow}Conversion cancelled, cleaning up...{creset}")
            self._discard_partial_output()
            sys.exit(130)

        output_path = self.path + self.filename_tmp
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            self._discard_partial_output()
            print(f"{cred}Conversion produced no output{creset}")
            return False

        # Give the new file the same permissions as the original
        try:
            shutil.copymode(self.path + self.filename_origin, output_path)
        except OSError:
            print(f"{cred}Could not copy permissions to: '{output_path}'{creset}")
        self.filename_new = self.filename_tmp
        self.filename_tmp = ""
        return True

    @staticmethod
    def detect_fferror(filepath):
        """Returns a string with the detected errors.

        Args:
            filepath (str): The full filepath of the video.

        Returns:
            str: The errors that have been found/happened.
            False: The lack of errors.
        """
        try:
            args = ["ffprobe", "-v", "error", str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            output = output.decode().strip()
            if len(output) > 0:
                return output
        except (subprocess.CalledProcessError, IndexError):
            return f'{cred}There seems to be a "subprocess.CalledProcessError" error with "{filepath}"{creset}'
        return False

    @staticmethod
    def detect_codec(filepath):
        """Returns a string with the detected codec.

        Args:
            filepath (str): The full filepath of the video.

        Returns:
            str: The codec that has been detected.
            False: An error in the codec fetching process.
        """
        output = False
        try:
            args = [
                "ffprobe",
                "-v",
                "quiet",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=codec_name",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(filepath),
            ]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            # Decoding from binary, stripping whitespace, keep only last line
            # in case ffprobe added error messages over the requested information
            output = output.decode().strip()
        except (subprocess.CalledProcessError, IndexError):
            return False
        return output

    @staticmethod
    def detect_resolution(filepath):
        """Returns a list with the detected width(0) and height(1).

        Args:
            filepath (str): The full filepath of the video.

        Returns:
            List: The detected width(0) and height(1).
            False: An error in the resolution fetching process.
        """
        try:
            args = [
                "ffprobe",
                "-v",
                "quiet",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=width,height",
                "-of",
                "csv=s=x:p=0",
                str(filepath),
            ]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            # Decoding from binary, stripping whitespace, keep only last line
            # in case ffprobe added error messages over the requested information
            output = output.decode().strip()
            # See if we got convertible data
            output = [int(output.split("x")[0]), int(output.split("x")[1])]
        except (subprocess.CalledProcessError, IndexError):
            return False
        return output[0], output[1]

    @staticmethod
    def detect_definition(filepath=False, width=False, height=False):
        """Returns a string with the detected definition corrected for dead space.

        Args:
            filepath (str): A string containing the full filepath.
            width (int): The width of the video.
            height (int): The height of the video.

        Returns:
            str: The classified definition in width(0) and height(1).
            False: An error in the process.
        """
        if filepath:
            width, height = Video.detect_resolution(filepath)
        if not width and not height:
            return False

        if width >= 2160 or height >= 2160:
            return "uhd"
        elif width >= 1440 or height >= 1080:
            return "1080p"
        elif width >= 1280 or height >= 720:
            return "720p"
        elif height >= 480:
            return "sd"
        return "subsd"

    @staticmethod
    def detect_filesize(filepath):
        """Returns an integer with size in MB.

        Args:
            filepath (str): A string containing the full filepath.

        Returns:
            int: The filesize in MB.
            False: An error in the process.
        """
        try:
            size = int(os.path.getsize(filepath) / 1024 / 1024)
        except OSError:
            return False
        return size
