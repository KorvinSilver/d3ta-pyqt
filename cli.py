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
import shutil
import sqlite3
import sys
import time
import urwid
from contextlib import contextmanager
from d3lib import edit
from d3lib.aes import *

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "0.9"
__email__ = "dev@korvin.eu"
__status__ = "Development"

selected_item = ""
text_entry = ""
option_back = "Back..."
option_delete = "Delete..."
option_delete_all = "Delete all..."
option_exit = "Exit..."
option_new_entry = "New entry..."
option_new_entry_with_hint = "New entry with hint..."
option_view_edit = "View/Edit..."
option_yes = "Yes"
option_yes_all = "Delete everything"
option_no = "No"
submenu_options = [option_back, option_view_edit, option_delete]


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
        print(f"'{db}' exists.")
        sys.exit(1)


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
        print("Invalid password.")


def datetime():
    """
    Returns the current date and time formatted like "2018-01-02 12:34:56"

    :return: formatted date and time
    :rtype: str
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def option_handler(button, tuple_):
    """
    Breaks the current loop, opens new widget or exits the program

    :param button: button clicked
    :type button: urwid.Button
    :param tuple_: holds the selected item, the sqlite3.Cursor, the table name
    and the password
    :type tuple_: tuple
    """
    item = tuple_[0]
    c = tuple_[1]
    tb = tuple_[2]
    psw = tuple_[3]

    global selected_item
    global option_new_entry, option_new_entry_with_hint, option_delete_all
    global option_view_edit, option_delete
    global option_yes, option_no, option_yes_all
    global text_entry

    # Create a new entry using the text editor
    if item == option_new_entry:
        # create entry
        text_entry = edit.main("ENTRY")
        # add it to the database
        add_entry(c, tb, datetime(), psw, text_entry)
    # Create a new entry with hint using the text editor
    elif item == option_new_entry_with_hint:
        # create hint
        hint = edit.main("HINT")
        # replace newline characters with space
        hint = hint.replace("\n", " ")
        # limit it to length 255
        hint = hint[:255]
        # create entry
        text_entry = edit.main("ENTRY")
        # Add entry with hint to database
        add_entry(c, tb, datetime(), psw, text_entry, hint)
    # Open existing entry in text editor
    elif item == option_view_edit:
        # get date from item's name
        dt = selected_item[:19]
        # get hint from item's name
        hint = selected_item[21:-1]
        # get decrypted text
        text_entry = single_entry(c, tb, dt, psw)
        # open decrypted text in text editor
        text_entry = edit.main(text_entry)
        # replace entry
        delete_entry(c, tb, dt)
        add_entry(c, tb, dt, psw, text_entry, hint)
    # Delete entry
    elif item == option_delete:
        # get date from item's name
        selected_item = selected_item[:19]
        # ask for confirmation
        loop(f"Delete {selected_item}?", [option_yes, option_no], c, tb, psw)
    # Confirmation to delete entry
    elif item == option_yes:
        delete_entry(c, tb, selected_item)
    # Delete all entries
    elif item == option_delete_all:
        # ask for confirmation
        loop(f"Delete everything?", [option_yes_all, option_no], c, tb, psw)
    # Confirmation to delete all entries
    elif item == option_yes_all:
        # recreate table in database
        delete_table(c, tb)
        create_main_table(c, tb)
    # No confirmation
    elif item == option_no:
        pass
    # Every other case, store item to selected_item so the program knows
    # when to exit
    else:
        selected_item = item
    # Exit current loop
    raise urwid.ExitMainLoop


def menu(title, items, c, tb, psw):
    """
    Creates the menu as buttons

    :param title: menu title
    :type title: str
    :param items: menu items
    :type items: list
    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param tb: table
    :type tb: str
    :param psw: password
    :type psw: str
    :return: list of menu items as buttons
    :rtype: urwid.SimpleListWalker
    """
    # Create menu body
    body = [urwid.Text(title), urwid.Divider()]
    for i in items:
        # Create button with menu item
        button = urwid.Button(i)
        if i == "":
            # don't connect the button if it's an empty string
            pass
        else:
            # connect the button to option_handler
            # pass in i, c, tb and psw as a tuple
            urwid.connect_signal(
                button, "click", option_handler, (i, c, tb, psw))
        # Append button to body
        body.append(urwid.AttrMap(button, None, focus_map="reversed"))
    return urwid.SimpleListWalker(body)


def make_overlay(body):
    """
    Create an overlay window with the menu items

    :param body: menu items
    :type body: urwid.ListBox
    :return: overlay window
    :rtype: urwid.Overlay
    """
    return urwid.Overlay(
        body, urwid.SolidFill("\N{DARK SHADE}"),  # unicode character U+2593
        align="center", valign="middle",
        width=("relative", 90), height=("relative", 90),
        min_width=20, min_height=8)


def loop(title, items, c, tb, psw):
    """
    Creates the main loop

    :param title: menu title
    :type title: str
    :param items: menu items
    :type items: list
    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param tb: table
    :type tb: str
    :param psw: password
    :type psw: str
    """
    # Create body
    body = urwid.ListBox(menu(title, items, c, tb, psw))
    # Create overlay
    overlay = make_overlay(body)
    # Create palette
    palette = [("reversed", "standout", "")]
    # Start main loop
    urwid.MainLoop(overlay, palette).run()


def run(c, tb, psw):
    """
    Run program

    :param c: sqlite3 Cursor instance
    :type c: sqlite3.Cursor
    :param tb: table
    :type tb: str
    :param psw: password
    :type psw: str
    """
    global option_new_entry, option_new_entry_with_hint, option_exit
    global option_delete_all, selected_item
    global submenu_options

    # Restart main loop until option_exit is clicked
    while selected_item != option_exit:
        # Create the list used in the main menu from the database
        items = []
        for item in all_entry_names(c, tb):
            # store as a string, e.g.: "2018-01-02 12:34:56 (hint)"
            items.append(f"{item[0]} ({item[1]})")
        # Add main menu options to the list
        items = [option_new_entry, option_new_entry_with_hint,
                 option_exit, ""] + items
        items += ["", "", option_delete_all]
        # Start main menu loop
        loop("D3TA", items, c, tb, psw)
        # If not a main menu option is selected, start another loop with
        #  selected_item and submenu_options
        if selected_item not in (
                "", option_new_entry, option_new_entry_with_hint, option_exit,
                option_delete_all):
            loop(selected_item, submenu_options, c, tb, psw)


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
        # ask to create backup and ask for confirmation
        print(f"Make sure you have a backup of '{database}' before "
              f"continuing.")
        make_backup = input("Create one now? (Y/n) ")
        if make_backup not in ("n", "N"):
            shutil.copyfile(database, database + ".bak")
            print(f"'{database}.bak' created.")
        ready = input("Ready to continue? (y/N) ")
        if ready not in ("y", "Y"):
            sys.exit(0)
        # open database
        with open_database(database) as cr:
            password = getpass.getpass("Old Password:")
            if valid_password(cr, password):
                # ask new password twice
                new_password = getpass.getpass("New Password:")
                re_check = getpass.getpass("New Password again:")
                if re_check == new_password:
                    print("Changing password, re-encrypting all entries.\n"
                          "This could take a while...")
                    change_password(cr, password, new_password, table)
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

        run(cr, table, password)
