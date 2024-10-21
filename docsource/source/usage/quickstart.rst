==========
Quickstart
==========

To use `mediacurator`, execute the following command structure:

.. code-block:: bash

    mediacurator <command> [options]

    mediacurator [list convert] [-del/--delete]
        [-i/--inputs any 3gp asf avi divx dv f4v flv gif m2ts m4v mkv mov mp4 mpeg mpg mts ogm ogv rm swf ts vid vob webm wmv]
        [-fl/--filters fferror old lowres hd 720p 1080p uhd mpeg mpeg4 x264 wmv3 wmv]
        [-o/--outputs mkv/mp4 x265/av1]
        [-p/--printop list formatted verbose]
        [-d/--dirs "/mnt/media/" "/mnt/media2/"]
        [-f/--files "file1.ext" "file2.ext"]

**Available commands:**
- `list`: List all videos with specified filters.
- `convert`: Convert videos to specified formats.

**Options:**

- `-del` or `--delete`: Delete found results after successful operations.
- `-i <input>` or `--inputs <input>`: Specify input file formats (default: `any`).
- `-fl <filter>` or `--filters <filter>`: Apply filters to the selection of videos.
- `-o <output>` or `--outputs <output>`: Specify output formats (default: `mkv`, `x265`).
- `-p <print_option>` or `--printop <print_option>`: Set print options (default: `list`).
- `-f <file>` or `--files <file>`: Specify files to process.
- `-d <directory>` or `--dirs <directory>`: Specify directories to process.

**For multiple files or filenames, use space-separated values ( ).**

**Default options:**

- `-i/--inputs any`
- `-fl/--filters`
- `-o/--outputs mkv x265`
- `-p/--printop list`

**Examples:**

The following examples demonstrate how to use `mediacurator` with the options listed above:

.. code-block:: bash

    # List all videos with an old codec in formatted format
    mediacurator list --filters old --printop formatted --dirs /mnt/media/ >> ../medlist.txt

    # Convert all videos with the MPEG4 codec to MP4 using the AV1 codec and delete the originals
    mediacurator convert --delete --filters mpeg4 --outputs av1,mp4 --dirs "/mnt/media/Movies/"

    # Convert any video with AVI or MPG extensions, print formatted text including FFmpeg's output, and then delete the originals
    mediacurator convert --delete --inputs avi,mpg --printop formatted,verbose --dirs /mnt/media/

For more examples, see :doc:`use_cases`.
