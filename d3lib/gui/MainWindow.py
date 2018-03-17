# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d3lib/gui/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 2, 3, 2, 3)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setFlat(True)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 1, 5, 1, 1)
        self.deleteAllButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteAllButton.setFlat(True)
        self.deleteAllButton.setObjectName("deleteAllButton")
        self.gridLayout.addWidget(self.deleteAllButton, 3, 2, 1, 1)
        self.newButton = QtWidgets.QPushButton(self.centralwidget)
        self.newButton.setFlat(True)
        self.newButton.setObjectName("newButton")
        self.gridLayout.addWidget(self.newButton, 1, 1, 1, 1)
        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setFlat(True)
        self.openButton.setObjectName("openButton")
        self.gridLayout.addWidget(self.openButton, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 3, 1, 1)
        self.newEntryButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newEntryButton.sizePolicy().hasHeightForWidth())
        self.newEntryButton.setSizePolicy(sizePolicy)
        self.newEntryButton.setFlat(True)
        self.newEntryButton.setObjectName("newEntryButton")
        self.gridLayout.addWidget(self.newEntryButton, 1, 3, 1, 1)
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setFlat(True)
        self.deleteButton.setObjectName("deleteButton")
        self.gridLayout.addWidget(self.deleteButton, 3, 1, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 2, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.exitButton = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.exitButton.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.exitButton.setObjectName("exitButton")
        self.verticalLayout.addWidget(self.exitButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.newAction = QtWidgets.QAction(MainWindow)
        self.newAction.setObjectName("newAction")
        self.openAction = QtWidgets.QAction(MainWindow)
        self.openAction.setObjectName("openAction")
        self.exitAction = QtWidgets.QAction(MainWindow)
        self.exitAction.setObjectName("exitAction")
        self.aboutD3TAAction = QtWidgets.QAction(MainWindow)
        self.aboutD3TAAction.setObjectName("aboutD3TAAction")
        self.aboutQt5Action = QtWidgets.QAction(MainWindow)
        self.aboutQt5Action.setObjectName("aboutQt5Action")
        self.actionD3TA_License = QtWidgets.QAction(MainWindow)
        self.actionD3TA_License.setObjectName("actionD3TA_License")
        self.actionPySide2_License = QtWidgets.QAction(MainWindow)
        self.actionPySide2_License.setObjectName("actionPySide2_License")
        self.licenseAction = QtWidgets.QAction(MainWindow)
        self.licenseAction.setObjectName("licenseAction")
        self.changePassAction = QtWidgets.QAction(MainWindow)
        self.changePassAction.setObjectName("changePassAction")
        self.licensePySide2Action = QtWidgets.QAction(MainWindow)
        self.licensePySide2Action.setObjectName("licensePySide2Action")
        self.newEntryAction = QtWidgets.QAction(MainWindow)
        self.newEntryAction.setObjectName("newEntryAction")
        self.saveAction = QtWidgets.QAction(MainWindow)
        self.saveAction.setObjectName("saveAction")
        self.deleteAction = QtWidgets.QAction(MainWindow)
        self.deleteAction.setObjectName("deleteAction")
        self.menuFile.addAction(self.newAction)
        self.menuFile.addAction(self.openAction)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.newEntryAction)
        self.menuFile.addAction(self.saveAction)
        self.menuFile.addAction(self.deleteAction)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.changePassAction)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.exitAction)
        self.menuHelp.addAction(self.licenseAction)
        self.menuHelp.addAction(self.aboutD3TAAction)
        self.menuHelp.addAction(self.aboutQt5Action)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "D3TA"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.deleteAllButton.setText(_translate("MainWindow", "Delete All"))
        self.newButton.setText(_translate("MainWindow", "New"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.newEntryButton.setText(_translate("MainWindow", "New Entry"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.newAction.setText(_translate("MainWindow", "Ne&w Diary"))
        self.newAction.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.openAction.setText(_translate("MainWindow", "&Open Diary"))
        self.openAction.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.exitAction.setText(_translate("MainWindow", "&Exit"))
        self.exitAction.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.aboutD3TAAction.setText(_translate("MainWindow", "&About D3TA"))
        self.aboutQt5Action.setText(_translate("MainWindow", "A&bout Qt5"))
        self.actionD3TA_License.setText(_translate("MainWindow", "D3TA License"))
        self.actionPySide2_License.setText(_translate("MainWindow", "PySide2 License"))
        self.licenseAction.setText(_translate("MainWindow", "&License"))
        self.changePassAction.setText(_translate("MainWindow", "&Change Password"))
        self.changePassAction.setShortcut(_translate("MainWindow", "Ctrl+F8"))
        self.licensePySide2Action.setText(_translate("MainWindow", "License &PySide2"))
        self.newEntryAction.setText(_translate("MainWindow", "&New Entry"))
        self.newEntryAction.setShortcut(_translate("MainWindow", "F2"))
        self.saveAction.setText(_translate("MainWindow", "&Save"))
        self.saveAction.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.deleteAction.setText(_translate("MainWindow", "&Delete"))
        self.deleteAction.setShortcut(_translate("MainWindow", "Ctrl+Del"))

