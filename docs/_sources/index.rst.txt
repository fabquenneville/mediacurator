========================================
Welcome to mediacurator's documentation!
========================================

mediacurator is a Python command line tool to manage a media database.

* List all the videos and their information with or without filters
* Batch find and repair/convert videos with encoding errors
* Batch recode videos to more modern codecs (x265 / AV1) based on filters: extensions, codecs, resolutions ...

The source code can be found on `GitHub <https://github.com/fabquenneville/mediacurator>`_

.. warning::

   **Breaking changes in version 1.0.1:**

   Starting with version 1.0.1, the command-line interface (CLI) has undergone major changes, and the usage is **not backwards-compatible** with previous versions.

   If you are using `mediacurator < 1.0.1`, please refer to the legacy documentation available below (:ref:`legacy_docs`).

----------------------------------------
Documentation
----------------------------------------

.. toctree::
   :maxdepth: 2
   :caption: Usage:

   usage/warnings
   usage/installation
   usage/quickstart
   usage/manual
   usage/use_cases
   usage/errors
   
.. toctree::
   :maxdepth: 1
   :caption: Release Notes:

   releasenotes/1.0.1-changelog

----

.. _legacy_docs:

----------------------------------------
Legacy Documentation (Pre 1.0)
----------------------------------------

.. warning::

   The following documentation is for versions prior to 1.0.1. It may contain features and usage instructions that are incompatible with the current version of mediacurator.

.. toctree::
   :maxdepth: 1
   :caption: Legacy Usage:

   legacy_usage/warnings
   legacy_usage/installation
   legacy_usage/quickstart
   legacy_usage/manual
   legacy_usage/use_cases
   legacy_usage/errors

.. toctree::
   :maxdepth: 1
   :caption: Legacy Release Notes:

   releasenotes/0.0.13-changelog
   releasenotes/0.0.12-changelog
   releasenotes/0.0.11-changelog
   releasenotes/0.0.10-changelog
   releasenotes/0.0.9-changelog
   releasenotes/0.0.8-changelog
   releasenotes/0.0.7-changelog
   releasenotes/0.0.6-changelog
   releasenotes/0.0.5-changelog
   releasenotes/0.0.4-changelog
   releasenotes/0.0.1-changelog

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
