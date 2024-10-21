======
Errors
======

.. warning::

   The following documentation is for versions prior to 1.0.1. It may contain features and usage instructions that are incompatible with the current version of mediacurator.

FFmpeg can detect quite a few errors in the encoding of your source video's encoding and can also be used to repair these errors.

Repairable Encoding Errors
--------------------------

Here are some example errors that mediacurator will print and can possibly repair by re-encoding:

* **"Referenced QT chapter track not found"**: Indicates that the video references a chapter that doesn't exist.
* **"Error, header damaged or not MPEG-4 header"**: The file's header is corrupted or missing.
* **"Header missing"**: The file lacks the necessary header information for decoding.
* **"SEI type"**: Issues related to SEI (Supplemental Enhancement Information) data.
* **"no frame!"**: No video frames available for processing.
* **"Error while decoding MPEG audio frame."**: Issues decoding the audio stream.
* **"big_values too big"**: Indicates that certain values in the file are larger than expected.
* ...

FFmpeg Issues
-------------

While using FFmpeg, you may encounter other errors (such as segfaults) depending on your version. Mediacurator will also print information when that occurs and will move on to the next video after cleaning up any failures.

If you experience these errors, consider the following steps:

* **Update FFmpeg**: Ensure you are using the latest version by downloading it from `ffmpeg.org <https://ffmpeg.org/download.html>`_, as many distributions provide outdated versions in their repositories.
* **Run with Verbose Option**: Execute mediacurator with the verbose print option, which will display the raw FFmpeg output for better troubleshooting.
* **Retry**: In my experience, some errors do not necessarily recur...

Other Bugs
----------

If you encounter other bugs, issues, or would like to suggest features, feel free to open a bug report on `GitHub <https://github.com/fabquenneville/mediacurator/issues>`_.

For further assistance, you can reach out through the GitHub repository or the project’s support channels.
