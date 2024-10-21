============
Installation
============

This package has been tested on GNU/Linux (e.g., Debian, Ubuntu, Fedora) and Windows, and requires FFmpeg to be installed. For now, it will be distributed on `GitHub <https://github.com/fabquenneville/mediacurator.git>`_.

Install FFmpeg
--------------

To install FFmpeg, you can follow the instructions for your platform:

- **On Debian and Ubuntu**: 
   .. code-block:: bash

      sudo apt update
      sudo apt install ffmpeg

- **On Fedora**: 
   .. code-block:: bash

      sudo dnf install ffmpeg

- **On Windows**:
  - Download the latest build from `FFmpeg <https://ffmpeg.org/download.html>`_.
  - Follow the installation instructions provided on the site.

To verify your FFmpeg installation, you can run:

.. code-block:: bash

   ffmpeg -version


Install from PyPi
-----------------

You can install the `mediacurator` package directly from PyPi using the following command:

.. code-block:: bash

   pip install mediacurator
