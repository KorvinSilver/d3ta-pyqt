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

import argparse
import bcrypt
import os
import pathlib
import shutil
import sys
import tarfile
import tempfile
# import urwid
# from getpass import getpass
from contextlib import contextmanager

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "0.1a"
__email__ = "dev@korvin.eu"
__status__ = "Development"


# TODO: re-encrypt all entries in change_password()

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
def manage_archive(arc):
    """
    Extracts the contents of an LZMA compressed tar archive to a temporary
    directory, yields, recreates the archive with the contents of that
    directory and removes it

    :param arc: an LZMA tar archive
    :type arc: str
    """
    # Create temp dir to store contents of archive
    with tempfile.TemporaryDirectory() as path:
        try:
            # open, extract and close archive
            t = tarfile.open(arc, "r:xz")
            t.extractall(path)
            t.close()
            yield path
        finally:
            # open for writing, add contents of temp dir and close archive
            t = tarfile.open(arc, "w:xz")
            t.add(path, arcname="/")
            t.close()


def create_archive(arc):
    """
    Creates a new, empty LZMA compressed tar archive.

    :param arc: archive to be created
    :type arc: str
    """
    t = tarfile.open(arc, "x:xz")
    t.close()


def path_to_files(path):
    """
    Returns a list of sorted filenames with path from the temporary directory
    created by manage_archive(), excluding the file "hash"

    :param path: path to temporary directory created by manage_archive()
    :type path: str
    :return: filenames with path
    :rtype: list
    """
    p = pathlib.Path(path)
    return sorted([str(i) for i in p.iterdir() if "/hash" not in str(i)])


def entry_name(ent, path):
    """
    Returns the filename from a file in the temporary directory created by
    manage_archive()

    :param ent: path to file
    :type ent: str
    :param path: path to temporary directory created by manage_archive()
    :type path: str
    :return: filename
    :rtype: str
    """
    return ent[len(path) + 1:]


def add_entry(ent, path):
    """
    Moves file to the temporary directory created by manage_archive()

    :param ent: file to be moved
    :type ent: str
    :param path: path to temporary directory created by manage_archive()
    :type path: str
    """
    # If entry already exists, replace it
    if os.path.isfile(ent) and os.path.isfile(os.path.join(path, ent)):
        os.remove(os.path.join(path, ent))
    try:
        shutil.move(ent, path)
    except shutil.Error:
        pass


def remove_entry(ent):
    """
    Removes an entry, i.e. a file from the temporary directory created by
    manage_archive()

    :param ent: file to be removed
    :type ent: str
    """
    os.remove(ent)


def password_match(psw, path):
    """
    Checks password against the stored salted hash

    :param psw: password
    :type psw: str
    :param path: path to temporary directory created by manage_archive()
    :type path: str
    :return: True|False
    :rtype: bool
    """
    with open(os.path.join(path, "hash")) as f:
        return bcrypt.checkpw(psw.encode("utf-8"), f.read().encode("utf-8"))


def store_new_hash(psw, path):
    """
    Stores a salted hash in a file created using a password

    :param psw: password
    :type psw: str
    :param path: path to temporary directory created by manage_archive()
    :type path: str
    """
    with open(os.path.join(path, "hash"), "w") as f:
        hsh = bcrypt.hashpw(psw.encode("utf-8"), bcrypt.gensalt())
        f.write(hsh.decode("utf-8"))


def change_password(old_psw, new_psw, path):
    # TODO: re-encrypt all entries
    if password_match(old_psw, path):
        store_new_hash(new_psw, path)
    else:
        print("Invalid password.")
        sys.exit(3)


if __name__ == "__main__":
    # Set variables with cli arguments, easier to modify later this way
    # change password - optional argument
    cp = "--change-password"
    # new archive - optional argument
    na = "--new-diary"
    # archive - positional argument
    ar = "diary"

    # Set usage message
    message = "%(prog)s [-h] [{} | {}] {}".format(cp, na, ar)

    parser = argparse.ArgumentParser(usage=message)
    parser.add_argument(ar, help="[path +] filename to your {}".format(ar))

    # Set custom attribute names for optional arguments
    parser.add_argument(na, action="store_true", dest="new_archive")
    parser.add_argument(cp, action="store_true", dest="change_pass")
    args = parser.parse_args()

    # Get positional argument's attribute with getattr() because it cannot be
    # set with dest
    archive = getattr(args, ar)

    # Exit if both optional arguments are present
    if args.new_archive and args.change_pass:
        parser.print_help()
        sys.exit(4)

    # Create new archive with --new-diary option
    if args.new_archive:
        # Ask for password, create archive, store hash and exit
        if not os.path.isfile(archive):
            # password = getpass("New password:")
            password = "pass"
            try:
                create_archive(archive)
            except PermissionError:
                print("You don't have permission to create this archive.")
                sys.exit(2)
            with manage_archive(archive) as extract_dir:
                store_new_hash(password, extract_dir)
            print("Archive created.")
            sys.exit(0)
        # Exit with code 1 if file already exists
        else:
            print("Archive already exists.")
            sys.exit(1)

    # Test archive
    # Exit with code 1 if archive doesn't exist
    if not os.path.isfile(archive):
        print("Archive doesn't exist")
        sys.exit(1)
    # Exit with code 2 if user doesn't have read or write permission
    if not (os.access(archive, os.R_OK) and os.access(archive, os.W_OK)):
        print("You don't have permission to manage this archive")
        sys.exit(2)

    with manage_archive(archive) as extract_dir:
        # Ask for password
        # password = getpass()
        password = "pass"
        # Check password, exit with code 3 if incorrect
        if not password_match(password, extract_dir):
            print("Invalid password.")
            sys.exit(3)

        # # Change password with --change-password option
        # if args.change_pass:
        #     # old_password = getpass("Old password:")
        #     old_password = "psw"
        #     # password = getpass("New password:")
        #     password = "pass"
        #     change_password(old_password, password, extract_dir)
        #     print("Password changed.")
        #     sys.exit(0)

        # Test full path and filename gathering
        files = path_to_files(extract_dir)
        print(files)

        # Test filename gathering
        entries = [entry_name(i, extract_dir) for i in files]
        print(entries)

        entry = "new_entry"

        # # Test entry addition
        # try:
        #     add_entry(entry, extract_dir)
        #     files = path_to_files(extract_dir)
        #     print(files)
        # except FileNotFoundError:
        #     print(entry, "doesn't exist")

        # Test entry removal
        try:
            remove_entry(os.path.join(extract_dir, entry))
            files = path_to_files(extract_dir)
            print(files)
        except FileNotFoundError:
            print(entry, "doesn't exist")
