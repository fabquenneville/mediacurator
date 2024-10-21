=========
Use cases
=========

The main reasons to use mediacurator would be the following:

* :ref:`list_cmd` on a video library such as:
    - How many videos of the lot are in HD vs standard or substandard definitions
    - What videos are in older codecs
    - Are there videos in the library with encoding or corruption errors
* :ref:`purge` selected videos in a media library
* :ref:`fferror` on selected videos in a media library
* :ref:`convert` videos from an old codec to `High Efficiency Video Coding <https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding>`_

.. _list_cmd:

Print information
-----------------

List all videos with old codec in formatted output

.. code-block:: bash

    mediacurator list --filters old --printop formatted --dirs "/mnt/media/" "/mnt/media2/"

List all videos with substandard definitions with a formatted output

.. code-block:: bash

    mediacurator list --filters subsd --printop formatted --dirs "/mnt/media/" "/mnt/media2/"

.. _purge:

Purge
-----

Please see :doc:`warnings`

List and delete all videos using the `Windows Media Video <https://en.wikipedia.org/wiki/Windows_Media_Video>`_ codecs

.. code-block:: bash

    mediacurator list --delete --filters wmv --dirs "/mnt/media/" "/mnt/media2/"

List and delete all videos using `Audio Video Interleave <https://en.wikipedia.org/wiki/Audio_Video_Interleave>`_

.. code-block:: bash

    mediacurator list --delete --inputs avi --dirs "/mnt/media/" "/mnt/media2/"

List and delete any videos with encoding errors

.. code-block:: bash

    mediacurator list --delete --filters fferror --dirs "/mnt/media/" "/mnt/media2/"

.. _fferror:

Batch repair encoding errors
----------------------------

List all videos with encoding errors

.. code-block:: bash

    mediacurator list --filters fferror --dirs "/mnt/media/" "/mnt/media2/"

List and delete any videos with encoding errors

.. code-block:: bash

    mediacurator list --delete --filters fferror --dirs "/mnt/media/" "/mnt/media2/"
    
Convert all videos with encoding errors to `High Efficiency Video Coding <https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding>`_ and delete the originals

.. code-block:: bash

    mediacurator convert --delete --filters fferror --dirs "/mnt/media/" "/mnt/media2/"

.. _convert:

Batch re-encode
---------------

Convert all videos with old codecs to `High Efficiency Video Coding <https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding>`_ to save space and delete the originals

.. code-block:: bash

    mediacurator convert --delete --filters old --dirs "/mnt/media/" "/mnt/media2/"
    
Convert all videos with the codec mpeg4 to an mkv container using the av1 video codec

.. code-block:: bash

    mediacurator convert --filters mpeg4 --outputs av1,mkv --dirs "/mnt/media/" "/mnt/media2/"
    
Convert any video with avi or mpg extensions, print formatted text including ffmpeg's output, and then delete the originals

.. code-block:: bash

    mediacurator convert --delete --inputs avi,mpg --printop formatted,verbose --dirs "/mnt/media/" "/mnt/media2/"
