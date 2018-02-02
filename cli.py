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
import getpass
import os
import sqlite3
import sys
import time
from contextlib import contextmanager
from cryptolib.aes import *

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "0.1a"
__email__ = "dev@korvin.eu"
__status__ = "Development"


# TODO: re-encrypt all entries in change_password()

# TODO: menu with urwid
# TODO: text editor with urwid

# TODO: menu option to create database
# TODO: menu option to delete database
# TODO: ask confirmation twice when deleting database

# TODO: menu option to create entry in database
# TODO: menu option to modify entry in database
# TODO: menu option to delete entry from database
# TODO: menu option to delete all entries from database
# TODO: ask confirmation when deleting entry
# TODO: ask confirmation twice when deleting all entries


def create_database(db, tb, psw):
    """
    Creates a new database file

    :param db: filename
    :type db: str
    :param tb: table name
    :type tb: str
    :param psw: password
    :type psw: str
    """
    # Create if doesn't exist
    if not os.path.exists(db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        # Create new table with name as value of 'tb'.
        # In that table, create columns date, hint and entry.
        # date is datetime type (i.e. with format 2018-01-02 12:34:56)
        # hint is tinytext type (max 255 characters)
        # entry is longtext type (max 4 294 967 295 characters)
        c.execute(f"CREATE TABLE {tb} (date datetime, hint tinytext, "
                  f"entry longtext)")
        # Create new table with name hash
        # In that table, create column hash
        # hash is text type (max 65 535 characters)
        c.execute("CREATE TABLE hash (hash text)")
        # Store salted hash generated from password in hash
        hashed = bcrypt.hashpw(psw.encode("utf-8"), bcrypt.gensalt())
        hashed = hashed.decode("utf-8")
        c.execute(f"INSERT INTO hash VALUES (\"{hashed}\")")
        conn.commit()
        c.close()
        conn.close()
    else:
        print(f"'{db}' exists.")
        sys.exit(1)


@contextmanager
def open_database(db):
    """
    Open database as a context manager

    :param db: filename
    :type db: str
    :return: generator iterator
    :rtype: sqlite3.Cursor
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    try:
        # Try to fetch something to see if sqlite3.DatabaseError gets raised
        c.fetchone()
        yield c
    except sqlite3.DatabaseError:
        print(f"'{db}' is not a database or you don't have the necessary "
              f"permissions.")
        sys.exit(2)
    finally:
        conn.commit()
        c.close()
        conn.close()


def add_entry(c, tb, dt, psw, ent, ht=""):
    """
    Adds a new row in table 'tb'

    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param tb: table
    :type tb: str
    :param dt: datetime
    :type dt: str
    :param psw: password
    :type psw: psw
    :param ent: entry
    :type ent: str
    :param ht: hint
    :type ht: str
    """
    # Check if row with 'datetime' exists
    c.execute(f"SELECT entry FROM {tb} WHERE date = '{dt}'")
    if c.fetchone() is None:
        # Encrypt entry
        ent = encrypt(psw, ent)
        # Store datetime, hint and encrypted entry
        c.execute(f"INSERT INTO {tb} VALUES ('{dt}', '{ht}', '{ent}')")
    else:
        print(f"Entry with {dt} already exists.")


def single_entry(c, tb, dt, psw):
    """
    Returns a decrypted entry from table 'tb'

    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param tb: table
    :type tb: str
    :param dt: datetime
    :type dt: str
    :param psw: password
    :type psw: str
    :return: decrypted entry
    :rtype: str
    """
    # Get the entry where its datetime matches 'dt'
    c.execute(f"SELECT entry FROM {tb} WHERE date = '{dt}'")
    return decrypt(psw, c.fetchone()[0])


def all_entry_names(c, tb):
    """
    Returns the names of all entries in table 'tb'

    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param tb: table
    :type tb: str
    :return: list of tuples containing a datetime and a hint
    :rtype: list
    """
    lst = []
    for ent in c.execute(f"SELECT * FROM {tb}"):
        lst.append((ent[0], ent[1]))
    return lst


def delete_entry(c, tb, dt):
    """
    Deletes an entry from table 'tb'

    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param tb: table
    :type tb: str
    :param dt: datetime
    :type dt: str
    """
    # Deletes an entry where its datetime matches 'dt'
    c.execute(f"DELETE FROM {tb} WHERE date = '{dt}'")


def delete_table(c, tb):
    """
    Deletes table 'tb' from database

    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param tb: table
    :type tb: str
    """
    c.execute(f"DELETE FROM {tb}")


def valid_password(c, psw):
    """
    Validates password

    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param psw: password
    :type psw: str
    :return: True|False
    :rtype: bool
    """
    # Get stored hash from table hash
    c.execute(f"SELECT hash FROM hash")
    hashed = (c.fetchone()[0]).encode("utf-8")
    return bcrypt.checkpw(psw.encode("utf-8"), hashed)


def change_password(c, old_psw, new_psw):
    """
    Changes password

    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param old_psw: old password
    :type old_psw: str
    :param new_psw: new password
    :type new_psw: str
    """
    if valid_password(c, old_psw):
        # Recreate table hash
        c.execute("DROP TABLE hash")
        c.execute("CREATE TABLE hash (hash text)")
        # Store salted hash from password
        hashed = bcrypt.hashpw(new_psw.encode("utf-8"), bcrypt.gensalt())
        hashed = hashed.decode("utf-8")
        c.execute(f"INSERT INTO hash VALUES (\"{hashed}\")")

        # TODO: re-encrypt all entries

    else:
        print("Invalid password.")


if __name__ == "__main__":
    # Set variables with cli arguments, easier to modify later this way
    # change password - optional argument
    cp = "--change-password"
    # new archive - optional argument
    nd = "--new-diary"
    # database - positional argument
    base = "diary"

    # Set usage message
    message = f"%(prog)s [-h] [{cp} | {nd}] {base}"
    parser = argparse.ArgumentParser(usage=message)
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
        parser.print_help()
        sys.exit(4)

    # Exit if database doesn't exist and not trying to create new
    if not os.path.isfile(database) and not args.new_database:
        print(f"'{database}' doesn't exist.")
        sys.exit(1)

    # Exit if trying to create new database but the path exists
    if os.path.exists(database) and args.new_database:
        print(f"'{database}' already exists.")
        sys.exit(1)

    # Create new database and exit
    if args.new_database:
        try:
            # ask password twice
            password = getpass.getpass()
            re_check = getpass.getpass("Password again:")
            if password == re_check:
                create_database(database, base, password)
                print(f"'{database}' created.")
                sys.exit(0)
            else:
                print("Passwords don't match.")
                sys.exit(1)
        except sqlite3.OperationalError:
            print(f"Unable to create '{database}'.\n"
                  f"Check path and permissions.")
            sys.exit(1)

    # Check permissions of database
    if not (os.access(database, os.R_OK) or os.access(database, os.W_OK)):
        print("You don't have the necessary permissions.")
        sys.exit(1)

    table = base

    # Change password and exit
    if args.change_pass:
        # open database
        with open_database(database) as cr:
            password = getpass.getpass("Old Password:")
            if valid_password(cr, password):
                # ask new password twice
                new_password = getpass.getpass("New Password:")
                re_check = getpass.getpass("New Password again:")
                if re_check == new_password:
                    change_password(cr, password, new_password)
                    print("Password changed.")
                    sys.exit(0)
                else:
                    print("Passwords don't match.")
                    sys.exit(1)
            else:
                print("Invalid password.")
    # Open database
    with open_database(database) as cr:
        password = getpass.getpass()
        if not valid_password(cr, password):
            print("Invalid password.")
            sys.exit(1)

        # Get date and time to store in database
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # add_entry(cr, table, datetime, password, "Hello, SQLite!", "hint")
        print(all_entry_names(cr, table))
        # print(single_entry(cr, table, "2018-02-02 10:33:27", password))
        # delete_entry(cr, table, "2018-02-02 10:32:59")
        # delete_table(cr, table)
