# mediacurator

mediacurator is a Python command line tool to manage a media database.

- List all the videos and their information with or without filters
- Batch find and repair/convert videos with encoding errors
- Batch recode videos to more modern codecs (x265 / AV1) based on filters: extensions, codecs, resolutions …

## Documentation

The documentation is available on the following [link](https://fabquenneville.github.io/mediacurator/)

## Releases

mediacurator can be installed via the following methods:

- APT repository for Debian/Ubuntu systems
- PyPi using pip

For detailed installation instructions, please visit the following links:

- [Installation Instructions](https://fabquenneville.github.io/mediacurator/usage/installation.html)
- [APT Repository](https://debrepo.fabq.ca/)
- [PyPi Page](https://pypi.org/project/mediacurator/)

## Usage

```bash
    mediacurator <command> [options]

    # Command options
    mediacurator [list convert] [-del/--delete/-delr/--delete-on-reduce]
        [
            -i/--inputs any 3g2 3gp amv asf avi dav divx dv f4v flv gif m1v m2p m2t m2ts m2v m4p m4v mkv mov mp4 mpe
                        mpeg mpg mpv mts mxf ogm ogv qt rm rmvb swf tod ts vid vob webm wm wmv wtv
        ]
        [-fl/--filters fferror old lowres hd 720p 1080p 2160p uhd 4k mpeg mpeg4 x264 wmv3 wmv]
        [-o/--outputs mkv/mp4 x265/av1/av2]
        [-p/--printop list formatted verbose]
        [--preset <name>] [--crf <value>]
        [-d/--dirs "/mnt/media/" "/mnt/media2/"]
        [-f/--files "file1.ext" "file2.ext"]
```

**Available commands:**

- `list`: List all videos with specified filters.
- `convert`: Convert videos to specified formats.

**Options:**

- `-del` or `--delete`: Delete found results after successful operations. **Use with caution**.
- `-delr` or `--delete-on-reduce`: Delete the original post conversion only if the new file is smaller. **Use with caution**.
- `-i <input>` or `--inputs <input>`: Specify input file formats (default: `any`).
- `-fl <filter>` or `--filters <filter>`: Apply filters to the selection of videos.
- `-o <output>` or `--outputs <output>`: Specify output formats (default: `mkv`, `x265`).
- `-p <print_option>` or `--printop <print_option>`: Set print options (default: `list`).
- `-f <file>` or `--files <file>`: Specify files to process.
- `-d <directory>` or `--dirs <directory>`: Specify directories to process.
- `--preset <name>`: Encoder preset for `convert` (x265 default: `medium`, av1 default: `6`).
- `--crf <value>`: Constant rate factor for `convert` (x265 default: `28`, av1 default: `30`). Lower is higher quality and larger files.

**For multiple files or filenames, use space-separated values ( ).**

**Default options (if not specified):**

- `-i/--inputs`: `any`
- `-fl/--filters`: (none)
- `-o/--outputs`: `mkv`, `x265`
- `-p/--printop`: `list`

### Examples

```bash
# List all videos with old codecs in formatted output
mediacurator list --filters old --printop formatted --dirs "/mnt/media/" "/mnt/media2/" >> ../medlist.txt

# Convert all MPEG4 videos to AV1 in MP4 format, and delete originals after conversion
mediacurator convert --delete --filters mpeg4 --outputs av1 mp4 --dirs "/mnt/media/" "/mnt/media2/"

# Convert videos with AVI or MPG extensions, print formatted and verbose output, and delete originals if size was reduced
mediacurator convert --delete-on-reduce --inputs avi mpg --printop formatted verbose --dirs "/mnt/media/" "/mnt/media2/"

# Convert to x265 with the slow preset and CRF 24 for higher quality
mediacurator convert --filters old --preset slow --crf 24 --dirs "/mnt/media/"
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
