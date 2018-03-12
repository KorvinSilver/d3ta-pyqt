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

import sys
from cli import table_name
from d3lib.gui import license_text
from d3lib.gui.MainWindow import Ui_MainWindow
from d3lib.gui.AboutDialog import Ui_Dialog
from d3lib.dbtools import (
    all_entry_names,
    open_database,
    valid_password,
    single_entry
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
        self.setWindowState(QtCore.Qt.WindowMaximized)

        def show_license():
            """Open a dialog window with the license"""
            dialog = LicenseText()
            dialog.exec_()

        entry_index_list = []
        password = ""
        database = ""
        table = ""

        # noinspection PyArgumentList
        def open_new():
            """Choose a file"""
            nonlocal database, table, password, entry_index_list
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
                        if valid_password(cr, password):
                            table = table_name()
                            for entry, hint in all_entry_names(cr, table):
                                if hint != "":
                                    self.listWidget.addItem(
                                        f"{entry} -- {hint}")
                                else:
                                    self.listWidget.addItem(f"{entry}")
                                entry_index_list.append(entry)
                        else:
                            msg = QtWidgets.QMessageBox()
                            msg.setText("Invalid password!")
                            msg.exec_()

        # Connect buttons and menu items
        self.exitAction.triggered.connect(self.close)
        self.exitButton.clicked.connect(self.close)

        self.openAction.triggered.connect(open_new)
        self.openButton.clicked.connect(open_new)

        self.licenseAction.triggered.connect(show_license)

        # Show entry
        def show_entry():
            """Display text belonging to selected entry"""
            nonlocal database, table, password, entry_index_list
            entry = self.listWidget.selectedIndexes()[0]
            entry = entry.row()
            date = entry_index_list[entry]

            with open_database(database) as cr:
                entry = single_entry(cr, table, date, password)
                self.textEdit.setText(str(entry))

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
