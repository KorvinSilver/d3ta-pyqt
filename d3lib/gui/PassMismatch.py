# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PassMismatch.ui'
#
# Created: Fri Mar  2 02:47:10 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DialogPassMismatch(object):
    def setupUi(self, DialogPassMismatch):
        DialogPassMismatch.setObjectName("DialogPassMismatch")
        DialogPassMismatch.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../img/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogPassMismatch.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogPassMismatch)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(DialogPassMismatch)
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogPassMismatch)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogPassMismatch)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DialogPassMismatch.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DialogPassMismatch.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogPassMismatch)

    def retranslateUi(self, DialogPassMismatch):
        DialogPassMismatch.setWindowTitle(QtWidgets.QApplication.translate("DialogPassMismatch", "Passwords don\'t match!", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("DialogPassMismatch", "Passwords don\'t match!", None, -1))

