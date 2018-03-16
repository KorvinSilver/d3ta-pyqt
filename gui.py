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

import hashlib
import os
import shutil
import sqlite3
import sys
import webbrowser
from cli import table_name
from d3lib.cmenu import datetime
from d3lib.dbtools import (
    add_entry,
    all_entry_names,
    change_password,
    create_database,
    delete_entry,
    open_database,
    single_entry,
    valid_password,
)
from d3lib.gui import license_text
from d3lib.gui.AboutDialog import Ui_Dialog
from d3lib.gui.MainWindow import Ui_MainWindow
from PySide2 import QtCore, QtGui, QtWidgets

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "1.0"
__email__ = "dev@korvin.eu"
__status__ = "Production"

# Declare variables with different initial values
# These will store hash sums of the db file and the backup db file
db_hash = "+"
bak_hash = "-"


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Center window
        self.setGeometry(QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight,
            QtCore.Qt.AlignCenter,
            self.size(),
            QtGui.qApp.desktop().availableGeometry()))

        # Maximize window
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Declare variables to hold information
        # title of each entry - date
        entry_date_list = []
        # title of each entry - hint, if any
        entry_hint_list = []
        # password
        password = ""
        # location of current database
        database = ""
        # get table name defined in cli.py
        table = table_name()
        db_error = "Invalid database or you don't have the necessary " \
                   "permissions to open it!"

        def change_pass():
            """Change password of database entries"""
            global db_hash, bak_hash
            nonlocal database, password, table

            # Don't do anything if there's no database open
            if database == "":
                return

            # Ask for password
            psw, flag = password_box("Change Password", "Current password:")

            # If Ok is pressed
            if flag:
                # Check if given password matches the original
                if psw == password:
                    # ask for new password if it is
                    new, flag = password_box("Change Password",
                                             "New password:")
                    # leave password change if Cancel is pressed
                    if not flag:
                        return
                    # ask for new password second time
                    confirm, flag = password_box("Change Password",
                                                 "Confirm password:")
                    # leave password change if Cancel is pressed
                    if not flag:
                        return
                    # if new passwords match
                    if new == confirm:
                        # backup database
                        backup = BackupMessageBox(database)
                        backup.exec_()
                        if db_hash == bak_hash:
                            msg_box("Backup file " + database + ".bak created")
                        else:
                            msg_box("Something went wrong! "
                                    "Password didn't change!")
                            return

                        # change password
                        change = PasswordChangeMessageBox(
                            database, table, password, new
                        )
                        change.exec_()
                        # display message of successful change
                        msg_box("Password changed.")
                        # clear listWidget and textEdit
                        # and make database path empty
                        self.listWidget.clear()
                        self.textEdit.setText("")
                        database = ""
                    else:
                        # if passwords don't match
                        # display message and leave password change
                        msg_box("Passwords don't match!")
                        return
                else:
                    # if given password doesn't match the original
                    # display message and leave password change
                    msg_box("Invalid password!")
                    return
            else:
                # leave password change if Cancel is pressed
                return

        def confirm_box(text, info_text, yes_button, no_button):
            """
            Displays a QMessageBox with buttons to confirm an action

            :param text: text to be set
            :type text: str
            :param info_text: informative text to be set
            :type info_text: str
            :param yes_button: button object to be used to confirm action
            :type yes_button: PySide2.QtWidgets.QMessageBox.StandardButton
            :param no_button: button object to be used to cancel action
            :type no_button: PySide2.QtWidgets.QMessageBox.StandardButton'
            :return: selected button
            :rtype: PySide2.QtWidgets.QMessageBox.StandardButton
            """
            dialog = QtWidgets.QMessageBox()
            dialog.setText(text)
            dialog.setInformativeText(info_text)
            dialog.setStandardButtons(
                yes_button | no_button)
            select = dialog.exec_()
            return select

        def confirm_exit():
            """Display a confirm exit dialog"""
            select = confirm_box(
                "Exit",
                "Are you sure you want to exit?",
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.Cancel)
            if select == QtWidgets.QMessageBox.Yes:
                self.close()

        def delete():
            """Delete an entry from the database"""
            nonlocal database, table, password, entry_date_list
            nonlocal entry_hint_list

            # Don't do anything if there's no database open
            if database == "":
                return
            # Don't do anything if there's nothing in the listWidget
            if not self.listWidget.selectedIndexes():
                return

            # Ask for confirmation
            select = confirm_box(
                "Delete Entry",
                "Do you want to delete entry?",
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.Cancel)

            if select == QtWidgets.QMessageBox.Yes:
                # get selected item's index
                index = self.listWidget.selectedIndexes()[0]
                index = index.row()
                # get date from date list based on index
                date = entry_date_list[index]
                # clear listWidget and textEdit
                self.listWidget.clear()
                self.textEdit.setText("")
                # delete entry and reload listWidget
                with open_database(database) as cr:
                    delete_entry(cr, table, date)
                    refresh_list_widget(
                        cr, table, entry_date_list, entry_hint_list)

        def delete_all():
            """Delete database file and recreate an empty one"""
            nonlocal database, table, password

            # Don't do anything if there's no database open
            if database == "":
                return

            # Ask for confirmation
            select = confirm_box(
                "Delete Database",
                "Do you want to delete database?",
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.Cancel)
            if select == QtWidgets.QMessageBox.Yes:
                # ask for confirmation a second time
                select = confirm_box(
                    "Delete Database",
                    "Are you sure? This cannot be undone.",
                    QtWidgets.QMessageBox.Yes,
                    QtWidgets.QMessageBox.Cancel)
                # delete database file and recreate an empty one
                if select == QtWidgets.QMessageBox.Yes:
                    os.remove(database)
                    create_database(database, table, password)
                    # clear listWidget and textEdit
                    self.listWidget.clear()
                    self.textEdit.setText("")

        def line_input(title, text):
            """
            Displays a QInputDialog to ask for user input

            :param title: window title
            :type title: str
            :param text: text to be displayed
            :type text: str
            :return: user input
            :rtype: str
            """
            # noinspection PyCallByClass
            return QtWidgets.QInputDialog.getText(self, title, text)

        def msg_box(text):
            """
            Displays a QMessageBox with a given message
            :param text: message
            :type text: str
            """
            msg = QtWidgets.QMessageBox()
            msg.setText(text)
            msg.exec_()

        def new_db():
            """Create a new database"""
            nonlocal table

            # Ask user to choose where to save the new file
            # noinspection PyCallByClass
            name = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save file", "", ".sqlite3")
            # name is now a tuple of filename and extension, merge them
            name = "".join(name)

            # If empty, leave db creation
            if name == "":
                return

            # If file already exists, show message and leave db creation
            if os.path.isfile(name):
                msg_box("File already exists!")
                return

            # Ask for password
            psw, flag = password_box("Password", "Password:")
            # If Ok is pressed
            if flag:
                # ask for confirmation
                confirm, flag = password_box("Password", "Confirm password:")
                # if Ok is pressed
                if flag:
                    # check if passwords match
                    if psw == confirm:
                        try:
                            # create new database and display message
                            create_database(name, table, psw)
                            msg_box(f"Database successfully created:\n{name}")
                        # if can't be created, display message
                        except sqlite3.OperationalError:
                            msg_box("Couldn't create new database!")
                    else:
                        # if passwords don't match, display message
                        msg_box("Passwords don't match!")
                        return
                else:
                    # leave db creation if Cancel is pressed
                    return
            else:
                # leave db creation if Cancel is pressed
                return

        def new_entry():
            """Create new entry in the database"""
            nonlocal database, table, password, entry_date_list
            nonlocal entry_hint_list

            # Don't do anything if there's no database open
            if database == "":
                return

            # Empty lists
            del entry_date_list[:]
            del entry_hint_list[:]
            # Clear listWidget and textEdit
            self.listWidget.clear()
            self.textEdit.setText("")
            # Ask for visible hint, don't check if Ok or Cancel was pressed
            # noinspection PyCallByClass
            hint, _ = line_input("Visible hint", "Visible hint:")
            # Get formatted date from d3lib.cmenu.py
            date = datetime()

            # Add new entry and regenerate listWidget
            with open_database(database) as cr:
                add_entry(cr, table, date, password, "", hint)
                refresh_list_widget(
                    cr, table, entry_date_list, entry_hint_list)
            # Set listWidget's first item as selected
            self.listWidget.setCurrentRow(0)

        def open_browser_d3ta():
            """Open the D3TA project's page in the default web browser"""
            webbrowser.open_new_tab("https://gitlab.com/KorvinSilver/d3ta")

        def open_browser_pyside2():
            """Open the PySide2 project's page in the default web browser"""
            webbrowser.open_new_tab("https://wiki.qt.io/PySide2")

        def open_new():
            """Choose a file"""
            nonlocal database, table, password, entry_date_list
            nonlocal entry_hint_list

            # Ask user to select a file,
            # don't check if Open or Cancel was pressed
            # noinspection PyArgumentList
            database, _ = QtWidgets.QFileDialog.getOpenFileName()

            # If a file was selected
            if database != "":
                try:
                    # Open database
                    with open_database(database) as cr:
                        # store already given password
                        password_of_opened_db = password
                        # ask for password
                        password, flag = password_box("Password", "Password:")
                        # if Ok is pressed
                        if flag:
                            # check if password is valid
                            if valid_password(cr, password):
                                # regenerate listWidget
                                refresh_list_widget(
                                    cr,
                                    table,
                                    entry_date_list,
                                    entry_hint_list)
                            # if invalid password
                            else:
                                # display message and restore password
                                msg_box("Invalid password!")
                                password = password_of_opened_db
                        else:
                            # if Cancel is pressed, restore password
                            password = password_of_opened_db
                except sqlite3.DatabaseError:
                    # Show error message if database can't be opened
                    msg_box(db_error)

        def password_box(title, text):
            """
            Displays a QInputDialog that asks for a password

            :param title: window title
            :type title: str
            :param text: text to be displayed
            :type text: str
            :return: password, and True or False depending on which button was
                     pressed, Ok or Cancel
            :rtype: str, bool
            """
            # noinspection PyCallByClass
            psw, fl = QtWidgets.QInputDialog.getText(
                self, title, text, QtWidgets.QLineEdit.Password)
            return psw, fl

        def refresh_list_widget(c, tb, edl, ehl):
            """
            Updates the QListWidget

            :param c: sqlite3 Cursor instance
            :type c: sqlite3 Cursor
            :param tb: table name
            :type tb: str
            :param edl: entry date list
            :type edl: list
            :param ehl: entry hint list
            :type ehl: list
            """
            # Empty lists
            del edl[:]
            del ehl[:]
            # Clear listWidget and textEdit
            self.listWidget.clear()
            self.textEdit.setText("")
            # Regenerate listWidget
            for e, h in all_entry_names(c, tb):
                if h != "":
                    # add date and hint
                    self.listWidget.addItem(f"{e} -- {h}")
                else:
                    # add hint
                    self.listWidget.addItem(f"{e}")
                # add date and hint to lists
                edl.append(e)
                ehl.append(h)

        def save_entry():
            """Save entry to the database"""
            nonlocal database, table, password, entry_date_list
            nonlocal entry_hint_list

            # Don't do anything if there's no database open
            if database == "":
                return
            # Don't do anything if listWidget is empty
            if not self.listWidget.selectedIndexes():
                return

            # Get the selected item's index
            index = self.listWidget.selectedIndexes()[0]
            index = index.row()
            # Get date and hint from lists based on index
            date = entry_date_list[index]
            hint = entry_hint_list[index]
            # Get the content of textEdit
            entry = self.textEdit.toPlainText()

            # Delete existing entry, if any, and create new entry
            with open_database(database) as cr:
                delete_entry(cr, table, date)
                add_entry(cr, table, date, password, entry, hint)

        def show_entry():
            """Display text belonging to selected entry"""
            nonlocal database, table, password, entry_date_list

            # Don't do anything if listWidget is empty
            if not self.listWidget.selectedIndexes():
                return

            # Get index of selected item
            index = self.listWidget.selectedIndexes()[0]
            index = index.row()
            # Get date based on index
            date = entry_date_list[index]

            # Get the text from selected entry and display it in textEdit
            with open_database(database) as cr:
                entry = single_entry(cr, table, date, password)
                self.textEdit.setText(entry)

        def show_license_apache():
            """Open a dialog window with the Apache 2 license"""
            dialog = LicenseTextApache()
            dialog.exec_()

        def show_license_lgpl():
            """Open a dialog window with the LGPL3 license"""
            dialog = LicenseTextLGPL()
            dialog.exec_()

        # Connect buttons, menu items and QListWidget selection
        self.aboutD3TAAction.triggered.connect(open_browser_d3ta)
        self.aboutPySide2Action.triggered.connect(open_browser_pyside2)

        self.changePassAction.triggered.connect(change_pass)

        self.deleteAllButton.clicked.connect(delete_all)
        self.deleteButton.clicked.connect(delete)

        self.exitAction.triggered.connect(confirm_exit)
        self.exitButton.clicked.connect(confirm_exit)

        self.licenseAction.triggered.connect(show_license_apache)
        self.licensePySide2Action.triggered.connect(show_license_lgpl)

        self.newAction.triggered.connect(new_db)
        self.newButton.clicked.connect(new_db)

        self.newEntryButton.clicked.connect(new_entry)

        self.openAction.triggered.connect(open_new)
        self.openButton.clicked.connect(open_new)

        self.saveButton.clicked.connect(save_entry)

        self.listWidget.itemSelectionChanged.connect(show_entry)


class LicenseTextApache(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(LicenseTextApache, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("License")
        self.textBrowser.setText(license_text.html_apache())
        self.okButton.clicked.connect(self.close)


class LicenseTextLGPL(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(LicenseTextLGPL, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("License")
        self.textBrowser.setText(license_text.html_lgpl())
        self.okButton.clicked.connect(self.close)


class BackingUp(QtCore.QThread):
    """Executes the copying of the database on a new thread"""
    sig = QtCore.Signal()

    def __init__(self, file):
        super(BackingUp, self).__init__()
        self.file = file

    def run(self):
        global db_hash
        global bak_hash

        def make_hash(file):
            """
            Creates an SHA3-256 sum from a file

            :param file: file to be hashed
            :type file: str
            :return: hexadecimal hash string
            :rtype: str
            """
            h = hashlib.sha3_256()
            with open(file, "rb") as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    h.update(data)
            return h.hexdigest()

        # hash database
        db_hash = make_hash(self.file)
        # create backup
        # noinspection PyBroadException
        try:
            shutil.copyfile(self.file, self.file + ".bak")
            # hash backup file
            bak_hash = make_hash(self.file + ".bak")
        except Exception:
            pass
        # send a signal when it's done
        # noinspection PyUnresolvedReferences
        self.sig.emit()


class BackupMessageBox(QtWidgets.QMessageBox):
    """Displays a QMessageBox while the database is being copied"""
    def __init__(self, file):
        super(BackupMessageBox, self).__init__()
        self.file = file
        self.setText("Backing up database. This might take a while...")
        # disable buttons
        self.setStandardButtons(0)
        self.backup = BackingUp(self.file)
        self.backup.start()
        # for some reason self.close doesn't work
        # noinspection PyUnresolvedReferences
        self.backup.sig.connect(self.reject)


class ChangingPassword(QtCore.QThread):
    """Executes the password change of the database on a new thread"""
    sig = QtCore.Signal()

    def __init__(self, file, table, old_pass, new_pass):
        super(ChangingPassword, self).__init__()
        self.file = file
        self.table = table
        self.old_pass = old_pass
        self.new_pass = new_pass

    def run(self):
        with open_database(self.file) as cr:
            change_password(cr, self.old_pass, self.new_pass, self.table)
        # send signal when it's done
        # noinspection PyUnresolvedReferences
        self.sig.emit()


class PasswordChangeMessageBox(QtWidgets.QMessageBox):
    """Displays a QMessageBox while the password change is running"""
    def __init__(self, file, table, old_pass, new_pass):
        super(PasswordChangeMessageBox, self).__init__()
        self.setText("Changing password. This might take a while...")
        # disable buttons
        self.setStandardButtons(0)
        self.pass_change = ChangingPassword(file, table, old_pass, new_pass)
        self.pass_change.start()
        # for some reason self.close doesn't work
        # noinspection PyUnresolvedReferences
        self.pass_change.sig.connect(self.reject)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
