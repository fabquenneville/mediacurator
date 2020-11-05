#!/usr/bin/env python3
'''Its a script!
    ./converter.py list -dir "/"
    ./converter.py convert -del -dir "/mnt/media/"

'''

import sys
import os
import subprocess
import distro
from pathlib import Path
from pprint import pprint
from hurry.filesize import size


def main():
    ffmpeg_version = detect_ffmpeg()
    if not ffmpeg_version:
        print("No ffmpeg version detected")
        exit()
    print(f"ffmpeg installed: {ffmpeg_version}")
    
    if len(sys.argv) >= 2:
        # Get command parameters
        directories = []
        inputs = []
        filters = []
        outputs = []
        for arg in sys.argv:
            if "-in:" in arg:
                inputs += arg[4:].split(",")
            elif "-filters:" in arg:
                filters += arg[9:].split(",")
            elif "-out:" in arg:
                outputs += arg[5:].split(",")
            elif "-dir:" in arg:
                directories += arg[5:].split(",")
        

        if sys.argv[1] == "list":
            if any("-file" in argv for argv in sys.argv):
                pass
            elif any("-dir" in argv for argv in sys.argv):
                videolist = []
                #directory = sys.argv[sys.argv.index("-dir") + 1]
                for directory in directories:
                    videolist += get_videolist(directory, inputs, filters)
                for video in videolist:
                    print(f"{get_codec(video)} - {video}")
            else:
                print("Missing directory: ")
        elif sys.argv[1] == "test":
            if any("-file" in argv for argv in sys.argv):
                pass
            elif any("-dir" in argv for argv in sys.argv):
                print(f"directories = {directories}, inputs = {inputs}, filters = {filters}, outputs = {outputs}")
                exit()
            else:
                print("Missing directory: ")

            
        elif sys.argv[1] == "convert":
            if any("-file" in argv for argv in sys.argv):
                video = sys.argv[sys.argv.index("-file") + 1]
                folder = str(video)[:str(video).rindex("/") + 1]
                oldfilename = str(video)[str(video).rindex("/") + 1:]
                newfilename = oldfilename[:-4] + ".mkv"
                if oldfilename == newfilename:
                    newfilename = oldfilename[:-4] + "[HEVC]"
                
                print(f"***********   converting {oldfilename} to {newfilename}   ***********")
                try:
                    if convert(folder + oldfilename, folder + newfilename):
                        subprocess.call(['chmod', '777', folder + newfilename])
                        if "-del" in sys.argv:
                            delete(folder + oldfilename)
                except:
                    delete(folder + newfilename)
                    return False
            elif any("-dir" in argv for argv in sys.argv):
                videolist = []
                for directory in directories:
                    videolist += get_videolist(directory, inputs, filters)
                counter = 0
                for video in videolist:
                    folder = str(video)[:str(video).rindex("/") + 1]
                    oldfilename = str(video)[str(video).rindex("/") + 1:]
                    newfilename = oldfilename[:-4] + ".mkv"
                    if oldfilename == newfilename:
                        newfilename = oldfilename[:-4] + "[HEVC]"

                    counter += 1
                    print(f"***********   convert {counter} of {len(videolist)}   ***********")
                    try:
                        if convert(folder + oldfilename, folder + newfilename):
                            if "-del" in sys.argv:
                                delete(folder + oldfilename)
                    except:
                        delete(folder + newfilename)
                        return False

def get_videolist(parentdir, inputs = ["any"], filters = []):
    print(f"Scanning files in {parentdir} for videos")
    videolist = []

    path = Path(parentdir)
    if "wmv" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[wW][mM][vV]"))
    if "avi" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[aA][vV][iI]"))
    if "mkv" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[mM][kK][vV]"))
    if "mp4" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[mM][pP]4"))
    if "m4v" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[mM]4[vV]"))
    if "flv" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[fF][lL][vV]"))
    if "mpg" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[mM][pP][gG]"))
    
    
    # Remove folders
    videolist_tmp = videolist
    videolist = [video for video in videolist_tmp if video.is_file()]

    # Filter the list for specifi codecs
    videolist_tmp = videolist
    print(f"Filtering {len(videolist)} videos for the requested parameters")
    videolist = []

    if "old" in filters:
        videolist += [video for video in videolist_tmp if get_codec(video) not in ["hevc", "av1"]]

    if "mpeg4" in filters or "mpeg" in filters:
        videolist += [video for video in videolist_tmp if get_codec(video) in ["mpeg4", "msmpeg4v3"]]

    if "mpeg" in filters:
        videolist += [video for video in videolist_tmp if get_codec(video) in ["mpeg1video"]]

    if "wmv3" in filters or "wmv" in filters:
        videolist += [video for video in videolist_tmp if get_codec(video) in ["wmv3"]]

    if "x264" in filters:
        videolist += [video for video in videolist_tmp if get_codec(video) in ["x264"]]
        
    print(f"Found {len(videolist)} videos for the requested parameters")
    return videolist


def get_codec(filename):
    try:
        args = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", str(filename)]
        output = subprocess.check_output(args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print(f"There seams to be an error with {filename}")
        return False
    return output.decode().strip()

def convert(oldfilename, newfilename):
    oldsize = size(Path(oldfilename).stat().st_size)
    print(f"Starting conversion of {oldfilename}({oldsize}) from {get_codec(oldfilename)} ...")

    # Preparing ffmpeg command and input file
    args = ['ffmpeg', '-i', oldfilename]

    # conversion options
    args += ['-c:v', 'libx265']
    args += ['-max_muxing_queue_size', '1000']

    # conversion output
    args += [newfilename]

    #args = ['ffmpeg', '-i', oldfilename, newfilename]
    try:
        if "-verbose" in sys.argv:
            subprocess.call(args)
        else:
            txt = subprocess.check_output(args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed {e}")
        return False
    else:
        newsize = size(Path(newfilename).stat().st_size)
        oldfilename = str(oldfilename)[str(oldfilename).rindex("/") + 1:]
        newfilename = str(newfilename)[str(newfilename).rindex("/") + 1:]
        print(f"Converted {oldfilename}({oldsize}) to {newfilename}({newsize}) successfully")
        return True

def delete(filename):
    try:
        os.remove(filename)
    except OSError:
        print(f"Error deleting {filename}")
        return False

    print(f"Deleted {filename}")
    return True

def detect_ffmpeg():
    try:
        txt = subprocess.check_output(['ffmpeg', '-version'], stderr=subprocess.STDOUT).decode()
        return txt.partition('\n')[0]
    except:
        return False

if __name__ == '__main__':
    main()
