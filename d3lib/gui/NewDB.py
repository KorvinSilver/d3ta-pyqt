# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewDB.ui'
#
# Created: Fri Mar  2 02:47:16 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DialogNew(object):
    def setupUi(self, DialogNew):
        DialogNew.setObjectName("DialogNew")
        DialogNew.resize(500, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../img/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogNew.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogNew)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelPass = QtWidgets.QLabel(DialogNew)
        self.labelPass.setObjectName("labelPass")
        self.gridLayout.addWidget(self.labelPass, 1, 0, 1, 1)
        self.labelFileName = QtWidgets.QLabel(DialogNew)
        self.labelFileName.setObjectName("labelFileName")
        self.gridLayout.addWidget(self.labelFileName, 0, 0, 1, 1)
        self.labelPassAgain = QtWidgets.QLabel(DialogNew)
        self.labelPassAgain.setObjectName("labelPassAgain")
        self.gridLayout.addWidget(self.labelPassAgain, 2, 0, 1, 1)
        self.lineEditFileName = QtWidgets.QLineEdit(DialogNew)
        self.lineEditFileName.setObjectName("lineEditFileName")
        self.gridLayout.addWidget(self.lineEditFileName, 0, 1, 1, 1)
        self.lineEditPassAgain = QtWidgets.QLineEdit(DialogNew)
        self.lineEditPassAgain.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditPassAgain.setObjectName("lineEditPassAgain")
        self.gridLayout.addWidget(self.lineEditPassAgain, 2, 1, 1, 1)
        self.lineEditPass = QtWidgets.QLineEdit(DialogNew)
        self.lineEditPass.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.lineEditPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditPass.setObjectName("lineEditPass")
        self.gridLayout.addWidget(self.lineEditPass, 1, 1, 1, 1)
        self.toolButton = QtWidgets.QToolButton(DialogNew)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogNew)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogNew)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DialogNew.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DialogNew.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogNew)

    def retranslateUi(self, DialogNew):
        DialogNew.setWindowTitle(QtWidgets.QApplication.translate("DialogNew", "D3TA -- New", None, -1))
        self.labelPass.setText(QtWidgets.QApplication.translate("DialogNew", "Password:", None, -1))
        self.labelFileName.setText(QtWidgets.QApplication.translate("DialogNew", "Filename:", None, -1))
        self.labelPassAgain.setText(QtWidgets.QApplication.translate("DialogNew", "Password again:", None, -1))
        self.toolButton.setText(QtWidgets.QApplication.translate("DialogNew", "...", None, -1))

