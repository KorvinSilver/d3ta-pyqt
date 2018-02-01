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


# TODO: store password's hash
# TODO: password validation
# TODO: password change

# TODO: menu with urwid
# TODO: text editor with urwid

# TODO: option to create database
# TODO: option to delete database
# TODO: ask confirmation twice when deleting database

# TODO: option to create entry in database
# TODO: option to modify entry in database
# TODO: option to delete entry from database
# TODO: option to delete all entries from database
# TODO: ask confirmation when deleting entry
# TODO: ask confirmation twice when deleting all entries


def create_database(db, tb):
    if not os.path.isfile(db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f"CREATE TABLE {tb} (date date, entry longtext)")
        conn.close()
    else:
        print(f"'{db}' exists.")
        sys.exit(1)


@contextmanager
def open_database(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    try:
        c.fetchone()
        yield c
    except sqlite3.DatabaseError:
        print(f"'{db}' is not a database.")
        sys.exit(2)
    finally:
        conn.commit()
        c.close()
        conn.close()


def add_entry(c, tb, dt, psw, ent):
    c.execute(f"SELECT entry FROM {tb} WHERE date = '{dt}'")
    if c.fetchone() is None:
        ent = encrypt(psw, ent)
        c.execute(f"INSERT INTO {tb} VALUES ('{dt}', '{ent}')")
    else:
        print(f"Entry with {dt} already exists.")


def retrieve_entry(c, tb, dt, psw):
    c.execute(f"SELECT entry FROM {tb} WHERE date = '{dt}'")
    return decrypt(psw, c.fetchone()[0])


def retrieve_all_entries(c, tb, psw):
    lst = []
    for ent in c.execute(f"SELECT * FROM {tb}"):
        lst.append((ent[0], decrypt(psw, ent[1])))
    return lst


def delete_entry(c, tb, dt):
    c.execute(f"DELETE FROM {tb} WHERE date = '{dt}'")


def delete_table(c, tb):
    c.execute(f"DELETE FROM {tb}")


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

    table = base
    password = "pass"
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # create_database(database, table)

    with open_database(database) as cr:
        # add_entry(cr, table, datetime, password, "Hello, SQLite!")
        print(retrieve_all_entries(cr, table, password))
        # print(retrieve_entry(cr, table, "2018-02-01 22:30:49", password))
        # delete_entry(cr, table, "2018-02-01 22:30:49")
        # delete_table(cr, table)
