# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConfirmExit.ui'
#
# Created: Fri Mar  2 02:47:29 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DialogConfirmExit(object):
    def setupUi(self, DialogConfirmExit):
        DialogConfirmExit.setObjectName("DialogConfirmExit")
        DialogConfirmExit.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../img/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogConfirmExit.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogConfirmExit)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(DialogConfirmExit)
        self.label.setInputMethodHints(QtCore.Qt.ImhNone)
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogConfirmExit)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogConfirmExit)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DialogConfirmExit.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DialogConfirmExit.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogConfirmExit)

    def retranslateUi(self, DialogConfirmExit):
        DialogConfirmExit.setWindowTitle(QtWidgets.QApplication.translate("DialogConfirmExit", "Exit D3TA?", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("DialogConfirmExit", "Are you sure you want to exit D3TA?", None, -1))

