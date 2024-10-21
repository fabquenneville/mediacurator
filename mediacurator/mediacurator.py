#!/usr/bin/env python3
'''
    mediacurator is a Python command line tool to manage a media database.
        * List all the videos and their information with or without filters
        * Batch find and repair/convert videos with encoding errors
        * Batch recode videos to more modern codecs (x265 / AV1) based on filters: extensions, codecs, resolutions...
        
    Examples:
    mediacurator list --filters old --printop formatted --dirs "/mnt/media/" "/mnt/media2/"
    mediacurator convert --delete --filters mpeg4 --outputs av1 mp4 --dirs "/mnt/media/" "/mnt/media2/"
    mediacurator convert --delete --inputs avi mpg --printop formatted verbose --dirs "/mnt/media/" "/mnt/media2/"
'''

# Normal import
try:
    from mediacurator.library.medialibrary import MediaLibrary
    from mediacurator.library.tools import check_ffmpeg, load_arguments
# Allow local import for development purposes
except ModuleNotFoundError:
    from library.medialibrary import MediaLibrary
    from library.tools import check_ffmpeg, load_arguments

# Import colorama for colored output
import colorama

colorama.init()

# Define color codes for colored output
cred = colorama.Fore.RED
creset = colorama.Fore.RESET


def main():
    '''
    Main function for mediacurator CLI tool.
    
    Handles command execution based on user input.
    '''

    print(f"{colorama.Style.BRIGHT}")

    # Check if ffmpeg is installed
    check_ffmpeg()

    # Load command-line arguments
    arguments = load_arguments()
    formatted = "formatted" in arguments.printop or "verbose" in arguments.printop

    try:
        # Initialize MediaLibrary with user-provided arguments
        medialibrary = MediaLibrary(files=arguments.files,
                                    directories=arguments.dirs,
                                    inputs=arguments.inputs,
                                    filters=arguments.filters,
                                    verbose='verbose' in arguments.printop)
        print(medialibrary)  # Optionally display the state of the MediaLibrary
    except ValueError as e:
        # Handle initialization errors
        print(f"{cred}ERROR: {str(e)}{creset}")
        return

    # Execute command based on the user's input
    if arguments.command == "list":
        medialibrary.list_videos(formatted, delete=arguments.delete)

    elif arguments.command == "test":
        medialibrary.test_videos(formatted, delete=arguments.delete)

    elif arguments.command == "convert":
        vcodec = "av1" if "av1" in arguments.outputs else "x265"
        medialibrary.convert_videos(vcodec,
                                    formatted=formatted,
                                    verbose="verbose" in arguments.printop,
                                    delete=arguments.delete)


if __name__ == '__main__':
    main()
