#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: D3TA (Dear Diary, Don't Tell Anyone)
Package: d3lib

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

import bcrypt
import os
import sqlite3
import sys
from contextlib import contextmanager
from .crypter import encrypt, decrypt

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "1.0"
__email__ = "dev@korvin.eu"
__status__ = "Production"


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
        sys.exit(f"'{db}' is not a database or you don't have the necessary "
                 f"permissions.")
    finally:
        conn.commit()
        c.close()
        conn.close()


def create_main_table(c, tb):
    """
    Create new table with name as value of 'tb'.
    In that table, create columns date, hint and entry:
    - date is datetime type (i.e. with format 2018-01-02 12:34:56)
    - hint is tinytext type (max 255 characters)
    - entry is longtext type (max 4 294 967 295 characters).

    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param tb: table
    :type tb: str
    """
    c.execute(f"CREATE TABLE {tb} (date datetime, hint tinytext, "
              f"entry longtext)")


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
        create_main_table(c, tb)
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
        sys.exit(f"'{db}' exists.")


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
        sys.exit(f"Entry with {dt} already exists.")


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
    for ent in c.execute(f"SELECT * FROM {tb} ORDER BY date DESC"):
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
    c.execute(f"DROP TABLE {tb}")


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


def change_password(c, old_psw, new_psw, tb):
    """
    Changes password by dropping then re-creating both the hash and the
    entry tables

    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param old_psw: old password
    :type old_psw: str
    :param new_psw: new password
    :type new_psw: str
    :param tb: table
    :type tb: str
    """
    if valid_password(c, old_psw):
        # Recreate table hash
        c.execute("DROP TABLE hash")
        c.execute("CREATE TABLE hash (hash text)")
        # Store salted hash from password
        hashed = bcrypt.hashpw(new_psw.encode("utf-8"), bcrypt.gensalt())
        hashed = hashed.decode("utf-8")
        c.execute(f"INSERT INTO hash VALUES (\"{hashed}\")")
        # Get the content of entry table
        c.execute(f"SELECT * FROM {tb}")
        to_re_encrypt = c.fetchall()
        # Delete table
        delete_table(c, tb)
        # Recreate table
        create_main_table(c, tb)
        # Re-encrypt all entries and fill table
        for i in to_re_encrypt:
            # Decrypt only, add_entry() will do the encrypting
            ent = decrypt(old_psw, i[2])
            add_entry(c, tb, i[0], new_psw, ent, i[1])
    else:
        sys.exit("Invalid password.")
