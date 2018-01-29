#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: D3TA (Dear Diary, Don't Tell Anyone)

Copyright 2018, Korvin F. Ezüst

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import pathlib
import shutil
import tarfile
import tempfile
import sys
# import urwid

from contextlib import contextmanager

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "0.1a"
__email__ = "dev@korvin.eu"
__status__ = "Development"


# TODO: menu with urwid
# TODO: text editor with urwid

# TODO: option to create archive
# TODO: option to delete archive
# TODO: ask confirmation twice when deleting archive

# TODO: option to create entry in archive
# TODO: option to modify entry in archive
# TODO: option to delete entry from archive
# TODO: option to delete all entries from archive
# TODO: ask confirmation when deleting entry
# TODO: ask confirmation twice when deleting all entries


@contextmanager
def repack_archive(arc):
    """
    Extracts the contents of an LZMA compressed tar archive to a temporary
    directory, yields the path to that directory then removes the archive
    and creates a new with the same name from the contents of the temporary
    directory.

    :param arc: an LZMA tar archive
    :type arc:  str
    """
    arc_dir = os.path.join(tempfile.gettempdir(), "d3ta_archive_extract")
    if os.path.isdir(arc_dir):
        shutil.rmtree(arc_dir)
    os.makedirs(arc_dir)
    try:
        t = tarfile.open(arc, "r:xz")
        t.extractall(arc_dir)
        t.close()
    finally:
        t = tarfile.open(arc, "w:xz")
        yield arc_dir
        t.add(arc_dir, arcname="/")
        t.close()
        shutil.rmtree(arc_dir)


def new_archive(arc):
    """
    Create a new, empty LZMA compressed tar archive.

    :param arc: archive to be created
    :type arc: str
    """
    t = tarfile.open(arc, "x:xz")
    t.close()


def get_entry_names(arc):
    """
    Get entry names in archive

    :param arc: an archive
    :type arc: str
    :return: entry names
    :rtype: list
    """
    t = tarfile.open(arc)
    names = t.getnames()
    try:
        names.remove("")
    except ValueError:
        pass
    names.sort()
    return names


def get_extracted_entries(arc):
    """
    Get full path and filename of files extracted from archive

    :param arc: an archive
    :type arc: str
    :return: list of names or error code on error
    :rtype: list|int
    """
    with repack_archive(arc) as arc_dir:
        p = pathlib.Path(arc_dir)
        names = [str(i) for i in p.iterdir() if i.is_file()]
        try:
            names.remove("")
        except ValueError:
            pass
        names.sort()
        return names


def add_entry(arc, ent):
    """
    Add file to archive.

    :param arc: archive
    :type arc: str
    :param ent: file to be added
    :type ent: str
    """
    if os.path.isfile(ent):
        with repack_archive(arc) as arc_dir:
            shutil.move(ent, os.path.join(arc_dir, ent))
    else:
        raise FileNotFoundError


def remove_entry(arc, ent):
    """
    Remove file from archive.

    :param arc: archive
    :type arc: str
    :param ent: file to be removed
    :type ent: str
    """
    with repack_archive(arc) as arc_dir:
        os.remove(os.path.join(arc_dir, ent))


if __name__ == "__main__":
    archive = "test_archive.tar.xz"

    # Exit with code 1 if archive doesn't exist
    if not os.path.isfile(archive):
        print("Archive doesn't exist.")
        sys.exit(1)

    # Test if archive is valid and user has permissions to read and write it
    try:
        with repack_archive(archive):
            pass
    except tarfile.ReadError:
        # Exit with code 2
        print("Archive could not be opened for reading.")
        sys.exit(2)
    except PermissionError:
        # Exit with code 3
        print("You don't have permission to manage this archive.")
        sys.exit(3)

    # Testing entry collection
    print("Testing entry collection:")
    entries = get_extracted_entries(archive)
    print(entries, end="\n\n")

    # Testing entry name collection
    print("Testing entry name collection:")
    entries = get_entry_names(archive)
    print(entries, end="\n\n")

    # Testing entry addition to archive
    print("Testing entry addition:")
    entry = "new_testfile"
    if not os.path.isfile(entry):
        print("Entry doesn't exist.\n")
    else:
        add_entry(archive, entry)
        entries = get_extracted_entries(archive)
        print(entries, end="\n\n")

    # Testing entry removal
    print("Testing entry removal:")
    try:
        entry = [i for i in get_extracted_entries(archive) if entry in i][0]
        remove_entry(archive, entry)
        print(get_entry_names(archive), end="\n\n")
    except IndexError:
        print("Entry is not in archive.\n")

    # Testing new archive creation
    print("Testing new archive creation:")
    new_arc = "/root/will_not_work"
    try:
        new_archive(new_arc)
    except PermissionError:
        print("You don't have permission to create this archive.")
