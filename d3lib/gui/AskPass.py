# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AskPass.ui'
#
# Created: Mon Mar 12 15:38:47 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AskPass(object):
    def setupUi(self, AskPass):
        AskPass.setObjectName("AskPass")
        AskPass.resize(400, 120)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../img/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AskPass.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(AskPass)
        self.verticalLayout.setObjectName("verticalLayout")
        self.passInput = QtWidgets.QLineEdit(AskPass)
        self.passInput.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.passInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passInput.setObjectName("passInput")
        self.verticalLayout.addWidget(self.passInput)
        self.buttonBox = QtWidgets.QDialogButtonBox(AskPass)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AskPass)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AskPass.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AskPass.reject)
        QtCore.QMetaObject.connectSlotsByName(AskPass)

    def retranslateUi(self, AskPass):
        AskPass.setWindowTitle(QtWidgets.QApplication.translate("AskPass", "Password", None, -1))

