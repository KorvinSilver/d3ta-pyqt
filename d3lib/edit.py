#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: D3TA (Dear Diary, Don't Tell Anyone)
Module: d3lib

This is a modified version of the Urwid example lazy text editor created by
Ian Ward. For the original, visit
https://github.com/urwid/urwid/blob/master/examples/edit.py

Copyright (C) 2018  Korvin F. Ezüst

This module is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This module is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import urwid

__authors__ = ["Ian Ward", "Korvin F. Ezüst"]
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "GNU Lesser General Public License 3.0"
__version__ = "1.0"
__maintainer__ = "Korvin F. Ezüst"
__email__ = "dev@korvin.eu"
__status__ = "Working"

new_text = ""


class LineWalker(urwid.ListWalker):
    """ListWalker-compatible class for lazily reading text."""

    index = 0

    def __init__(self, txt):
        self.text = txt.split("\n")
        self.lines = []
        self.focus = 0

    def get_focus(self):
        return self._get_at_pos(self.focus)

    def set_focus(self, focus):
        self.focus = focus
        self._modified()

    def get_next(self, start_from):
        return self._get_at_pos(start_from + 1)

    def get_prev(self, start_from):
        return self._get_at_pos(start_from - 1)

    def read_next_line(self, index):
        """Get next item from the text list."""

        try:
            next_line = self.text[index]
        except IndexError:
            next_line = "EOF"

        if next_line == "EOF":
            # no newline on last line of text
            next_line = ""
            self.text = None

        expanded = next_line.expandtabs()

        edit = urwid.Edit("", expanded, allow_tab=True)
        edit.set_edit_pos(0)
        edit.original_text = next_line
        self.lines.append(edit)

        return next_line

    def _get_at_pos(self, pos):
        """Return a widget for the line number passed."""

        if pos < 0:
            # line 0 is the start of the text, no more above
            return None, None

        if len(self.lines) > pos:
            # we have that line so return it
            return self.lines[pos], pos

        if self.text is None:
            # text is over, so there are no more lines
            return None, None

        assert pos == len(self.lines), "out of order request?"

        self.read_next_line(pos)

        return self.lines[-1], pos

    def split_focus(self):
        """Divide the focus edit widget at the cursor location."""

        focus = self.lines[self.focus]
        pos = focus.edit_pos
        edit = urwid.Edit("", focus.edit_text[pos:], allow_tab=True)
        edit.original_text = ""
        focus.set_edit_text(focus.edit_text[:pos])
        edit.set_edit_pos(0)
        self.lines.insert(self.focus + 1, edit)

    def combine_focus_with_prev(self):
        """Combine the focus edit widget with the one above."""

        above, ignore = self.get_prev(self.focus)
        if above is None:
            # already at the top
            return

        focus = self.lines[self.focus]
        above.set_edit_pos(len(above.edit_text))
        above.set_edit_text(above.edit_text + focus.edit_text)
        del self.lines[self.focus]
        self.focus -= 1

    def combine_focus_with_next(self):
        """Combine the focus edit widget with the one below."""

        below, ignore = self.get_next(self.focus)
        if below is None:
            # already at bottom
            return

        focus = self.lines[self.focus]
        focus.set_edit_text(focus.edit_text + below.edit_text)
        del self.lines[self.focus + 1]


class EditDisplay:
    palette = [
        ('body', 'default', 'default'),
        ('foot', 'light gray', 'black', 'bold'),
        ('key', 'light gray', 'black', 'underline'),
    ]

    footer_text = ('foot', [
        "Text Editor    ",
        ('key', "F8"), ": save and quit",
    ])

    def __init__(self, txt):
        self.save_name = txt
        self.walker = LineWalker(txt)
        self.listbox = urwid.ListBox(self.walker)
        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text),
                                     "foot")
        self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'),
                                footer=self.footer)

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.palette,
                                   unhandled_input=self.unhandled_keypress)
        self.loop.run()

    def unhandled_keypress(self, k):
        """Last resort for keypresses."""

        global new_text

        if k == "f8":
            self.save_text()
            raise urwid.ExitMainLoop()
        elif k == "delete":
            # delete at end of line
            self.walker.combine_focus_with_next()
        elif k == "backspace":
            # backspace at beginning of line
            self.walker.combine_focus_with_prev()
        elif k == "enter":
            # start new line
            self.walker.split_focus()
            # move the cursor to the new line and reset pref_col
            self.loop.process_input(["down", "home"])
        elif k == "right":
            w, pos = self.walker.get_focus()
            w, pos = self.walker.get_next(pos)
            if w:
                self.listbox.set_focus(pos, 'above')
                self.loop.process_input(["home"])
        elif k == "left":
            w, pos = self.walker.get_focus()
            w, pos = self.walker.get_prev(pos)
            if w:
                self.listbox.set_focus(pos, 'below')
                self.loop.process_input(["end"])
        else:
            return
        return True

    def save_text(self):
        """Save the text to global variable."""

        global new_text
        new_text = ""

        lst = []
        walk = self.walker
        index = 0
        for index, edit in enumerate(walk.lines):
            # collect the text already stored in edit widgets
            if edit.original_text.expandtabs() == edit.edit_text:
                lst.append(edit.original_text)
            else:
                lst.append(re_tab(edit.edit_text))

        # then the rest
        while walk.text is not None:
            index += 1
            lst.append(walk.read_next_line(index))

        for i in lst:
            new_text += i + "\n"
        new_text = new_text.strip("\n")


def re_tab(s):
    """Return a tabbed string from an expanded one."""
    l = []
    p = 0
    for i in range(8, len(s), 8):
        if s[i - 2:i] == "  ":
            # collapse two or more spaces into a tab
            l.append(s[p:i].rstrip() + "\t")
            p = i

    if p == 0:
        return s
    else:
        l.append(s[p:])
        return "".join(l)


def main(txt):
    global new_text
    EditDisplay(txt).main()
    return new_text


if __name__ == "__main__":
    text = "Hello\nمرحبا\nਸਤ ਸ੍ਰੀ ਅਕਾਲ\nสวัสดี\n你好\nこんにちは"
    main(text)
    print(new_text)
