#!/usr/bin/env python3
"""
mediacurator is a Python command line tool to manage a media database.
    * List all the videos and their information with or without filters
    * Batch find and repair/convert videos with encoding errors
    * Batch recode videos to more modern codecs (x265 / AV1 / AV2) based on filters: extensions, codecs, resolutions...

Examples:
mediacurator list --filters old --printop formatted --dirs "/mnt/media/" "/mnt/media2/"
mediacurator convert --delete --filters mpeg4 --outputs av1 mp4 --dirs "/mnt/media/" "/mnt/media2/"
mediacurator convert --delete --inputs avi mpg --printop formatted verbose --dirs "/mnt/media/" "/mnt/media2/"
"""

import sys

# Normal import
try:
    from mediacurator.library.medialibrary import MediaLibrary
    from mediacurator.library.tools import (
        check_ffmpeg,
        check_quality_options,
        find_encoder,
        load_arguments,
    )
# Allow local import for development purposes
except ModuleNotFoundError:
    from library.medialibrary import MediaLibrary
    from library.tools import (
        check_ffmpeg,
        check_quality_options,
        find_encoder,
        load_arguments,
    )

# Import colorama for colored output
import colorama

colorama.init()

# Define color codes for colored output
cred = colorama.Fore.RED
creset = colorama.Fore.RESET


def main():
    """
    Main function for mediacurator CLI tool.

    Handles command execution based on user input.
    """

    print(f"{colorama.Style.BRIGHT}")

    # Check if ffmpeg is installed
    check_ffmpeg()

    # Load command-line arguments
    arguments = load_arguments()
    formatted = "formatted" in arguments.printop or "verbose" in arguments.printop

    # Pick the target codec (av2 > av1 > x265) and fail early, before scanning
    # the library, if it can't be encoded by this ffmpeg build
    outputs = [output.lower() for output in arguments.outputs]
    if "av2" in outputs:
        vcodec = "av2"
    elif "av1" in outputs:
        vcodec = "av1"
    else:
        vcodec = "x265"

    if arguments.command == "convert":
        error = check_quality_options(vcodec, arguments.preset, arguments.crf)
        if error:
            print(f"{cred}ERROR: {error}{creset}")
            sys.exit(1)

    if arguments.command == "convert" and vcodec == "av2" and not find_encoder("av2"):
        print(
            f"{cred}ERROR: this ffmpeg build has no AV2 encoder (AV2 support in "
            f"ffmpeg is still pending). Use an ffmpeg build that has one, or "
            f"choose av1 / x265.{creset}"
        )
        sys.exit(1)

    try:
        # Initialize MediaLibrary with user-provided arguments
        medialibrary = MediaLibrary(
            files=arguments.files,
            directories=arguments.dirs,
            inputs=arguments.inputs,
            filters=arguments.filters,
            verbose="verbose" in arguments.printop,
        )
        print(medialibrary)  # Optionally display the state of the MediaLibrary
    except ValueError as e:
        # Handle initialization errors
        print(f"{cred}ERROR: {str(e)}{creset}")
        sys.exit(1)

    # Execute command based on the user's input
    if arguments.command == "list":
        medialibrary.list_videos(formatted, delete=arguments.delete)

    elif arguments.command == "test":
        medialibrary.test_videos(formatted, delete=arguments.delete)

    elif arguments.command == "convert":
        medialibrary.convert_videos(
            vcodec,
            formatted=formatted,
            verbose="verbose" in arguments.printop,
            delete=arguments.delete,
            delete_on_reduce=arguments.delete_on_reduce,
            preset=arguments.preset,
            crf=arguments.crf,
        )


if __name__ == "__main__":
    main()
