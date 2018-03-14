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

import os
import sys
import sqlite3
import webbrowser
from cli import table_name
from d3lib.cmenu import datetime
from d3lib.gui import license_text
from d3lib.gui.MainWindow import Ui_MainWindow
from d3lib.gui.AboutDialog import Ui_Dialog
from d3lib.dbtools import (
    all_entry_names,
    open_database,
    valid_password,
    single_entry,
    delete_entry,
    add_entry,
    create_database,
    change_password
)
from PySide2 import QtCore, QtGui, QtWidgets

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "0.1a"
__email__ = "dev@korvin.eu"
__status__ = "Development"


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
        # self.setWindowState(QtCore.Qt.WindowMaximized)

        def show_license():
            """Open a dialog window with the license"""
            dialog = LicenseText()
            dialog.exec_()

        entry_date_list = []
        entry_hint_list = []
        password = ""
        database = ""
        table = table_name()

        def msg_box(text):
            """
            Displays a QMessageBox with a given message
            :param text: message
            :type text: str
            """
            msg = QtWidgets.QMessageBox()
            msg.setText(text)
            msg.exec_()

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
            del edl[:]
            del ehl[:]
            self.listWidget.clear()
            self.textEdit.setText("")
            for e, h in all_entry_names(c, tb):
                if h != "":
                    self.listWidget.addItem(f"{e} -- {h}")
                else:
                    self.listWidget.addItem(f"{e}")
                edl.append(e)
                ehl.append(h)

        def open_new():
            """Choose a file"""
            nonlocal database, table, password, entry_date_list
            nonlocal entry_hint_list
            # noinspection PyArgumentList
            database, _ = QtWidgets.QFileDialog.getOpenFileName()

            if database != "":
                with open_database(database) as cr:
                    password_of_opened_db = password
                    password, flag = password_box("Password", "Password:")
                    if flag:
                        if valid_password(cr, password):
                            refresh_list_widget(
                                cr, table, entry_date_list, entry_hint_list)
                        else:
                            msg_box("Invalid password!")
                            password = password_of_opened_db
                    else:
                        password = password_of_opened_db

        def save_entry():
            """Save entry to the database"""
            nonlocal database, table, password, entry_date_list
            nonlocal entry_hint_list
            if database == "":
                return
            if not self.listWidget.selectedIndexes():
                return
            index = self.listWidget.selectedIndexes()[0]
            index = index.row()
            date = entry_date_list[index]
            hint = entry_hint_list[index]
            entry = self.textEdit.toPlainText()

            with open_database(database) as cr:
                delete_entry(cr, table, date)
                add_entry(cr, table, date, password, entry, hint)

        def new_entry():
            """Create new entry in the database"""
            nonlocal database, table, password, entry_date_list
            nonlocal entry_hint_list
            if database == "":
                return
            del entry_date_list[:]
            del entry_hint_list[:]
            self.textEdit.setText("")
            # noinspection PyCallByClass
            hint, _ = line_input("Visible hint", "Visible hint:")
            date = datetime()
            self.listWidget.clear()
            with open_database(database) as cr:
                add_entry(cr, table, date, password, "", hint)
                refresh_list_widget(
                    cr, table, entry_date_list, entry_hint_list)
            self.listWidget.setCurrentRow(0)

        def delete():
            """Delete an entry from the database"""
            nonlocal database, table, password, entry_date_list
            nonlocal entry_hint_list
            if database == "":
                return
            if not self.listWidget.selectedIndexes():
                return
            select = confirm_box(
                "Delete Entry",
                "Do you want to delete entry?",
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.Cancel)
            if select == QtWidgets.QMessageBox.Yes:
                index = self.listWidget.selectedIndexes()[0]
                index = index.row()
                date = entry_date_list[index]
                self.listWidget.clear()
                self.textEdit.setText("")
                with open_database(database) as cr:
                    delete_entry(cr, table, date)
                    refresh_list_widget(
                        cr, table, entry_date_list, entry_hint_list)

        def delete_all():
            """Delete database file and recreate an empty one"""
            nonlocal database, table, password
            if database == "":
                return
            select = confirm_box(
                "Delete Database",
                "Do you want to delete database?",
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.Cancel)
            if select == QtWidgets.QMessageBox.Yes:
                select = confirm_box(
                    "Delete Database",
                    "Are you sure? This cannot be undone.",
                    QtWidgets.QMessageBox.Yes,
                    QtWidgets.QMessageBox.Cancel)
                if select == QtWidgets.QMessageBox.Yes:
                    os.remove(database)
                    create_database(database, table, password)
                    self.listWidget.clear()
                    self.textEdit.setText("")

        def show_entry():
            """Display text belonging to selected entry"""
            nonlocal database, table, password, entry_date_list
            if not self.listWidget.selectedIndexes():
                return
            index = self.listWidget.selectedIndexes()[0]
            index = index.row()
            date = entry_date_list[index]

            with open_database(database) as cr:
                entry = single_entry(cr, table, date, password)
                self.textEdit.setText(entry)

        def open_browser_pyside2():
            """Open the PySide2 project's page in the default web browser"""
            webbrowser.open_new_tab("https://wiki.qt.io/PySide2")

        def open_browser_d3ta():
            """Open the D3TA project's page in the default web browser"""
            webbrowser.open_new_tab("https://gitlab.com/KorvinSilver/d3ta")

        def change_pass():
            """Change password of database entries"""
            nonlocal database, password, table
            psw, flag = password_box("Change Password", "Current password:")
            if flag:
                if psw == password:
                    new, flag = password_box("Change Password",
                                             "New password:")
                    if not flag:
                        return
                    confirm, flag = password_box("Change Password",
                                                 "Confirm password:")
                    if not flag:
                        return
                    if new == confirm:
                        with open_database(database) as cr:
                            change_password(cr, psw, new, table)
                        msg_box("Password changed.")
                        self.listWidget.clear()
                        self.textEdit.setText("")
                        database = ""
                    else:
                        msg_box("Passwords don't match!")
                        return
                else:
                    msg_box("Invalid password!")
                    return
            else:
                return

        def confirm_exit():
            """Display a confirm exit dialog"""
            select = confirm_box(
                "Exit",
                "Are you sure you want to exit?",
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.Cancel)
            if select == QtWidgets.QMessageBox.Yes:
                self.close()

        def new_db():
            """Create a new database"""
            nonlocal table
            # noinspection PyCallByClass
            name = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save file", "", ".sqlite3")
            name = "".join(name)
            if os.path.isfile(name):
                msg_box("File already exists!")
                return
            psw, flag = password_box("Password", "Password:")
            if flag:
                confirm, flag = password_box("Password", "Confirm password:")
                if flag:
                    if psw == confirm:
                        try:
                            create_database(name, table, "pass")
                            msg_box(f"Database successfully created:\n{name}")
                        except sqlite3.OperationalError:
                            msg_box("Couldn't create new database!")
                    else:
                        msg_box("Passwords don't match!")
                        return
                else:
                    return
            else:
                return

        # Connect buttons, menu items and QListWidget selection
        self.exitAction.triggered.connect(confirm_exit)
        self.exitButton.clicked.connect(confirm_exit)

        self.newButton.clicked.connect(new_db)
        self.newAction.triggered.connect(new_db)

        self.openAction.triggered.connect(open_new)
        self.openButton.clicked.connect(open_new)

        self.saveButton.clicked.connect(save_entry)
        self.newEntryButton.clicked.connect(new_entry)

        self.deleteButton.clicked.connect(delete)
        self.deleteAllButton.clicked.connect(delete_all)

        self.aboutD3TAAction.triggered.connect(open_browser_d3ta)
        self.aboutPySide2Action.triggered.connect(open_browser_pyside2)
        self.licenseAction.triggered.connect(show_license)

        self.changePassAction.triggered.connect(change_pass)

        self.listWidget.itemSelectionChanged.connect(show_entry)


class LicenseText(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(LicenseText, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("License")
        self.textBrowser.setText(license_text.html_text())
        self.okButton.clicked.connect(self.close)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
