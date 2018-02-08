#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: urwid_examples

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

import urwid

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "0.1a"
__email__ = "dev@korvin.eu"
__status__ = "Development"

selected_item = ""
option_back = "Back..."
option_delete = "Delete..."
option_delete_all = "Delete all..."
option_exit = "Exit..."
option_new_entry = "New entry..."
option_view_edit = "View/Edit..."
submenu_options = [option_back, option_view_edit, option_delete]

# TODO: handle each option_ as needed
# TODO: make the top menu persistent


def leave(button, item):
    """
    Exit program
    TODO: only exit with option_exit

    :param button: button clicked
    :type button: urwid.Button
    :param item: item chosen
    :type item: str
    """
    global selected_item, option_new_entry, option_exit, option_delete_all
    if item in (option_new_entry, option_exit, option_delete_all, ""):
        raise urwid.ExitMainLoop
    selected_item = item
    raise urwid.ExitMainLoop


def menu(title, items):
    """
    Creates the menu as buttons

    :param title: menu title
    :type title: str
    :param items: menu items
    :type items: list
    :return: list of menu items as buttons
    :rtype: urwid.SimpleListWalker
    """
    menu_items = [urwid.Text(title), urwid.Divider()]
    for i in items:
        button = urwid.Button(i)
        urwid.connect_signal(button, "click", leave, i)
        menu_items.append(urwid.AttrMap(button, None, focus_map="reversed"))
    return urwid.SimpleListWalker(menu_items)


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


def loop(title, items):
    """
    Creates the main loop

    :param title: menu title
    :type title: str
    :param items: menu items
    :type items: list
    """
    body = urwid.ListBox(menu(title, items))
    overlay = make_overlay(body)
    palette = [("reversed", "standout", "")]
    urwid.MainLoop(overlay, palette).run()


ships = ["New entry...", "Exit", "", "Andromeda Ascendant", "Deep Space 9",
         "Babylon 5", "Event Horizon", "", "", "Delete all..."]
loop("Ships", ships)

if selected_item != "":
    loop(selected_item, submenu_options)
