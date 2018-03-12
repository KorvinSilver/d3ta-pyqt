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

        # noinspection PyArgumentList
        def open_new():
            """Choose a file"""
            nonlocal database, table, password, entry_date_list
            nonlocal entry_hint_list
            database, _ = QtWidgets.QFileDialog.getOpenFileName()

            if database != "":
                with open_database(database) as cr:
                    # noinspection PyCallByClass
                    password, flag = QtWidgets.QInputDialog.getText(
                        self,
                        "Password",
                        "Password:",
                        QtWidgets.QLineEdit.Password)
                    if flag:
                        self.listWidget.clear()
                        self.textEdit.setText("")
                        if valid_password(cr, password):
                            for entry, hint in all_entry_names(cr, table):
                                if hint != "":
                                    self.listWidget.addItem(
                                        f"{entry} -- {hint}")
                                else:
                                    self.listWidget.addItem(f"{entry}")
                                entry_date_list.append(entry)
                                entry_hint_list.append(hint)
                        else:
                            msg = QtWidgets.QMessageBox()
                            msg.setText("Invalid password!")
                            msg.exec_()

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
            hint, _ = QtWidgets.QInputDialog.getText(
                self,
                "Visible hint",
                "Visible hint:")
            date = datetime()
            self.listWidget.clear()
            with open_database(database) as cr:
                add_entry(cr, table, date, password, "", hint)
                for entry, hint in all_entry_names(cr, table):
                    if hint != "":
                        self.listWidget.addItem(
                            f"{entry} -- {hint}")
                    else:
                        self.listWidget.addItem(f"{entry}")
                    entry_date_list.append(entry)
                    entry_hint_list.append(hint)
            self.listWidget.setCurrentRow(0)

        def delete():
            """Delete an entry from the database"""
            nonlocal database, table, password, entry_date_list
            nonlocal entry_hint_list
            if database == "":
                return
            if not self.listWidget.selectedIndexes():
                return
            confirm = QtWidgets.QMessageBox()
            confirm.setText("Delete Entry")
            confirm.setInformativeText("Do you want to delete entry?")
            confirm.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
            select = confirm.exec_()
            if select == QtWidgets.QMessageBox.Yes:
                index = self.listWidget.selectedIndexes()[0]
                index = index.row()
                date = entry_date_list[index]
                self.listWidget.clear()
                self.textEdit.setText("")
                with open_database(database) as cr:
                    delete_entry(cr, table, date)
                    del entry_date_list[:]
                    del entry_hint_list[:]
                    for entry, hint in all_entry_names(cr, table):
                        if hint != "":
                            self.listWidget.addItem(
                                f"{entry} -- {hint}")
                        else:
                            self.listWidget.addItem(f"{entry}")
                        entry_date_list.append(entry)
                        entry_hint_list.append(hint)

        def delete_all():
            nonlocal database, table, password
            if database == "":
                return
            confirm = QtWidgets.QMessageBox()
            confirm.setText("Delete Database")
            confirm.setInformativeText("Do you want to delete the database?")
            confirm.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
            select = confirm.exec_()
            if select == QtWidgets.QMessageBox.Yes:
                confirm = QtWidgets.QMessageBox()
                confirm.setText("Delete Database")
                confirm.setInformativeText(
                    "Are you sure? This cannot be undone.")
                confirm.setStandardButtons(
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
                select = confirm.exec_()
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

        # Connect buttons, menu items and QListWidget selection
        self.exitAction.triggered.connect(self.close)
        self.exitButton.clicked.connect(self.close)

        self.openAction.triggered.connect(open_new)
        self.openButton.clicked.connect(open_new)

        self.saveButton.clicked.connect(save_entry)
        self.newEntryButton.clicked.connect(new_entry)

        self.deleteButton.clicked.connect(delete)
        self.deleteAllButton.clicked.connect(delete_all)

        self.licenseAction.triggered.connect(show_license)

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
