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
import getpass
import os
import shutil
import sqlite3
import sys
from d3lib.cmenu import run
from d3lib.dbtools import (
    open_database,
    create_database,
    valid_password,
    change_password)

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "0.9"
__email__ = "dev@korvin.eu"
__status__ = "Development"


def table_name():
    """
    Return main table name. Using function to let other scripts know it, too

    :return: main table name
    :rtype: str
    """
    return "diary"


if __name__ == "__main__":
    # Set variables with cli arguments, easier to modify later this way
    # change password - optional argument
    cp = "--change-password"
    # new archive - optional argument
    nd = "--new-database"
    # database - positional argument
    base = "database"
    # Set the main table name inside the database
    table = table_name()
    # make base name available to other scripts
    program_name = "D3TA (Dear Diary, Don't Tell Anyone)"

    # Set usage message
    message = f"%(prog)s [-h] [{cp} | {nd}] {base}"
    parser = argparse.ArgumentParser(usage=message, description=program_name)
    parser.add_argument(base, help=f"[path +] filename to your {base}")

    # Set custom attribute names for optional arguments
    parser.add_argument(nd, action="store_true", dest="new_database")
    parser.add_argument(cp, action="store_true", dest="change_pass")
    args = parser.parse_args()

    # Get positional argument's attribute with getattr() because it cannot be
    # set with dest
    database = getattr(args, base)

    # Exit if both optional arguments are present
    if args.new_database and args.change_pass:
        sys.exit(parser.print_help())

    # Exit if database doesn't exist and not trying to create new
    if not os.path.isfile(database) and not args.new_database:
        sys.exit(f"'{database}' doesn't exist.")

    # Exit if trying to create new database but the path exists
    if os.path.exists(database) and args.new_database:
        sys.exit(f"'{database}' already exists.")

    # Create new database and exit
    if args.new_database:
        try:
            # ask password twice
            password = getpass.getpass()
            re_check = getpass.getpass("Password again: ")
            if password == re_check:
                create_database(database, table, password)
                sys.exit(f"'{database}' created.")
            else:
                sys.exit("Passwords don't match.")
        except sqlite3.OperationalError:
            sys.exit(f"Unable to create '{database}'.\n"
                     f"Check path and permissions.")

    # Check permissions of database
    if not (os.access(database, os.R_OK) or os.access(database, os.W_OK)):
        sys.exit("You don't have the necessary permissions.")

    # Change password and exit
    if args.change_pass:
        # ask to create backup and ask for confirmation
        print(f"Make sure you have a backup of '{database}' before "
              f"continuing.")
        make_backup = input("Create one now? (Y/n) ")
        if make_backup not in ("n", "N"):
            shutil.copyfile(database, database + ".bak")
            print(f"'{database}.bak' created.")
        ready = input("Ready to continue? (y/N) ")
        if ready not in ("y", "Y"):
            sys.exit()
        # open database
        with open_database(database) as cr:
            password = getpass.getpass("Old Password: ")
            if valid_password(cr, password):
                # ask new password twice
                new_password = getpass.getpass("New Password: ")
                re_check = getpass.getpass("New Password again: ")
                if re_check == new_password:
                    print("Changing password, re-encrypting all entries.\n"
                          "This could take a while...")
                    change_password(cr, password, new_password, table)
                    sys.exit("Password changed.")
                else:
                    sys.exit("Passwords don't match.")
            else:
                sys.exit("Invalid password.")
    # Open database
    try:
        with open_database(database) as cr:
            password = getpass.getpass()
            if not valid_password(cr, password):
                sys.exit("Invalid password.")

            run(cr, table, password)
    except sqlite3.DatabaseError:
        sys.exit(f"{database} is not a valid database or "
                 f"you don't have the necessary permissions to open it.")
