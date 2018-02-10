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

import time
import urwid
from .dbtools import (
    create_main_table,
    add_entry,
    single_entry,
    all_entry_names,
    delete_entry,
    delete_table)
from .text import edit

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
        selected_item = ""
    # No confirmation
    elif item == option_no:
        raise urwid.ExitMainLoop
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
