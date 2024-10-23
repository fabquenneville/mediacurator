#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mediacurator",
    version="1.0.1",
    author="Fabrice Quenneville",
    author_email="fabrice@fabq.ca",
    url="https://github.com/fabquenneville/mediacurator",
    download_url="https://pypi.python.org/pypi/mediacurator",
    project_urls={
        "Bug Tracker": "https://github.com/fabquenneville/mediacurator/issues",
        "Documentation": "https://fabquenneville.github.io/mediacurator/",
        "Source Code": "https://github.com/fabquenneville/mediacurator",
    },
    description=
    "mediacurator is a Python command line tool to manage a media database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Multimedia :: Video :: Conversion",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    entry_points={
        'console_scripts': ['mediacurator=mediacurator.mediacurator:main'],
    },
    keywords=[
        "codecs", "filters", "video", "x265", "av1", "media-database",
        "python-command", "hevc", "multimedia", "video-processing"
    ],
    install_requires=["pathlib", "colorama", "argcomplete"],
    license='GPL-3.0',
    license_files=('LICENSE', ),
    python_requires='>=3.6',
    platforms='any',
    zip_safe=True,
)
