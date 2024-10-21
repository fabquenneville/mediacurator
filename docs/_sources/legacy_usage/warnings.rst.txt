========
Warnings
========

.. warning::

   The following documentation is for versions prior to 1.0.1. It may contain features and usage instructions that are incompatible with the current version of mediacurator.

.. warning::

   Before using the **delete feature**, we strongly recommend running several dry runs to get acquainted with `mediacurator`, as incorrect usage can cause irreversible damage to your media library.

The `-del` flag will **permanently delete** files, so it is crucial to ensure that the command is executed correctly. Below are some examples of how the delete feature works.

Example use Cases for the `-del` Flag
-----------------------------------------

1. **Delete all non-HD (low-resolution) videos in a folder:**

.. code-block:: bash

    mediacurator list -del -filters:lowres  -dirs:"/mnt/media/"

2. **Delete all substandard quality videos in a folder:**

.. code-block:: bash

    mediacurator list -del -filters:subsd  -dirs:"/mnt/media/"

.. image:: ../_static/Legacy-Screenshot-delete.png
    :width: 600
    :alt: Deleting videos

3. **Delete all videos in a folder with encoding errors:**

.. code-block:: bash

    mediacurator list -del -filters:fferror  -dirs:"/mnt/media/"

4. **Convert (repair) and then delete all videos in a folder with encoding errors:**

.. code-block:: bash

    mediacurator convert -del -filters:fferror  -dirs:"/mnt/media/"

5. **Delete all videos in a folder:**

.. code-block:: bash

    mediacurator list -del -filters:lowres  -dirs:"/mnt/media/"

Important Notes
---------------

- **Irreversibility**: All of these commands involve permanent deletion. Once a file is deleted using the `-del` flag, it cannot be recovered.
- **Run without `-del` first**: Always perform several dry runs by omitting the `-del` flag to ensure that the correct files are selected for deletion. Familiarizing yourself with the tool before using destructive commands is essential to avoid unintended consequences.
- **Specific File Selection**: If you're unsure about applying filters to an entire directory, you can use the `-files` option to target individual files for deletion or conversion, further reducing the risk of unintended deletions.
- **Backup Recommendation**: Before running any commands with the `-del` flag, it is a good practice to back up your media library or the specific directories being processed, especially if they contain valuable or irreplaceable files.

Dry run example (without deletion)
----------------------------------

.. code-block:: bash

    mediacurator list -filters:lowres -dirs:"/mnt/media/"

Make sure you carefully verify the output and files selected during the dry runs to prevent accidental data loss.
