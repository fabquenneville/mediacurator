============
Installation
============

.. _install_toc:

Table of contents
-----------------

* :ref:`install_about`
* :ref:`install_apt`
* :ref:`install_pypi`
* :ref:`install_ffmpeg`

.. _install_about:

About mediacurator's installation
---------------------------------

This package has been tested on GNU/Linux (e.g., Debian, Ubuntu, Fedora) and Windows, and requires FFmpeg to be installed. For now, it will be distributed on `GitHub <https://github.com/fabquenneville/mediacurator.git>`_.

.. _install_apt:

Install from APT Repository
----------------------------

The `mediacurator` package is now available through an APT repository. To install it along with all its dependencies (including Python, required Python packages, and FFmpeg) on a Debian/Ubuntu compatible system, follow these steps:

1. Add the APT repository to your system by following the instructions at the `repository homepage <https://debrepo.fabq.ca/>`_.

2. Update your package list:

   .. code-block:: bash

      sudo apt update

3. Install `mediacurator`:

   .. code-block:: bash

      sudo apt install -y mediacurator

This will automatically install the `mediacurator` package and all its dependencies.

.. _install_pypi:

Install from PyPi
-----------------

You can install the `mediacurator` package directly from PyPi using the following command:

.. code-block:: bash

   pip install mediacurator

**Note:** If FFmpeg is not already installed, please refer to the instructions in the :ref:`install_ffmpeg` section.

.. _install_ffmpeg:

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
