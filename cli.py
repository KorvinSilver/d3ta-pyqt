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
import shutil
import tarfile
import tempfile
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
    with tempfile.TemporaryDirectory() as tmp:
        try:
            t = tarfile.open(arc, "r:xz")
            t.extractall(tmp)
            t.close()
        finally:
            t = tarfile.open(arc, "w:xz")
            yield tmp
            t.add(tmp, arcname="/")
            t.close()


def new_archive(arc):
    """
    Create a new, empty LZMA compressed tar archive.

    :param arc: archive to be created
    :type arc: str
    """
    t = tarfile.open(arc, "x:xz")
    t.close()


def get_entries(arc):
    """
    Get filenames from archive.

    :param arc: an LZMA compressed archive
    :type arc: str
    :return: list of names or error code on error
    :rtype: list|int
    """
    t = tarfile.open(arc, "r:xz")
    names = t.getnames()
    t.close()
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


def wrapper(func, *args):
    try:
        return func(*args)
    except tarfile.ReadError:
        return 1
    except PermissionError:
        return 2
    except FileExistsError:
        return 3
    except FileNotFoundError:
        return 4


if __name__ == "__main__":
    archive = "test_archive.tar.xz"

    # Testing entry collection
    entries = wrapper(get_entries, archive)
    if entries == 1:
        print("Archive could not be opened for reading.")
    elif entries == 2:
        print("You don't have permission to open this archive.")
    elif entries == 4:
        print("Archive doesn't exist.")
    else:
        print(entries)

    # Testing entry addition to archive
    entry = "new_entry"
    result = wrapper(add_entry, archive, entry)
    if result == 2:
        print("You don't have permission to add entries to this archive.")
    elif result == 4:
        print("Entry doesn't exist.")
    else:
        print(result)

    # Testing entry removal from archive
    entry = "file_beta"
    result = wrapper(remove_entry, archive, entry)
    if result == 2:
        print("You don't have permission to remove entries from this archive")

    # Testing archive creation
    result = wrapper(new_archive, "/root/will_not_work")
    if result == 2:
        print("You don't have permission to create this archive")
    elif result == 3:
        print("This archive already exists")
