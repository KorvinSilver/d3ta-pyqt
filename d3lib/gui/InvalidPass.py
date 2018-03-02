# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InvalidPass.ui'
#
# Created: Fri Mar  2 02:47:23 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DialogInvalidPass(object):
    def setupUi(self, DialogInvalidPass):
        DialogInvalidPass.setObjectName("DialogInvalidPass")
        DialogInvalidPass.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../img/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogInvalidPass.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogInvalidPass)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(DialogInvalidPass)
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogInvalidPass)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogInvalidPass)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DialogInvalidPass.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DialogInvalidPass.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogInvalidPass)

    def retranslateUi(self, DialogInvalidPass):
        DialogInvalidPass.setWindowTitle(QtWidgets.QApplication.translate("DialogInvalidPass", "Invalid password!", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("DialogInvalidPass", "Invalid password!", None, -1))

