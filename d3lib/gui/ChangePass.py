# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChangePass.ui'
#
# Created: Fri Mar  2 02:47:35 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DialogNewPass(object):
    def setupUi(self, DialogNewPass):
        DialogNewPass.setObjectName("DialogNewPass")
        DialogNewPass.resize(500, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../img/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogNewPass.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogNewPass)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.labelFileName_4 = QtWidgets.QLabel(DialogNewPass)
        self.labelFileName_4.setObjectName("labelFileName_4")
        self.gridLayout_4.addWidget(self.labelFileName_4, 0, 0, 1, 1)
        self.labelPassAgain_4 = QtWidgets.QLabel(DialogNewPass)
        self.labelPassAgain_4.setObjectName("labelPassAgain_4")
        self.gridLayout_4.addWidget(self.labelPassAgain_4, 2, 0, 1, 1)
        self.lineEditOldPass = QtWidgets.QLineEdit(DialogNewPass)
        self.lineEditOldPass.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.lineEditOldPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditOldPass.setObjectName("lineEditOldPass")
        self.gridLayout_4.addWidget(self.lineEditOldPass, 0, 1, 1, 1)
        self.lineEditNewPassAgain = QtWidgets.QLineEdit(DialogNewPass)
        self.lineEditNewPassAgain.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditNewPassAgain.setObjectName("lineEditNewPassAgain")
        self.gridLayout_4.addWidget(self.lineEditNewPassAgain, 2, 1, 1, 1)
        self.lineEditNewPass = QtWidgets.QLineEdit(DialogNewPass)
        self.lineEditNewPass.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.lineEditNewPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditNewPass.setObjectName("lineEditNewPass")
        self.gridLayout_4.addWidget(self.lineEditNewPass, 1, 1, 1, 1)
        self.labelPass_4 = QtWidgets.QLabel(DialogNewPass)
        self.labelPass_4.setObjectName("labelPass_4")
        self.gridLayout_4.addWidget(self.labelPass_4, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogNewPass)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogNewPass)
        QtCore.QMetaObject.connectSlotsByName(DialogNewPass)

    def retranslateUi(self, DialogNewPass):
        DialogNewPass.setWindowTitle(QtWidgets.QApplication.translate("DialogNewPass", "D3TA -- Change Password", None, -1))
        self.labelFileName_4.setText(QtWidgets.QApplication.translate("DialogNewPass", "Old Password:", None, -1))
        self.labelPassAgain_4.setText(QtWidgets.QApplication.translate("DialogNewPass", "New password again:", None, -1))
        self.labelPass_4.setText(QtWidgets.QApplication.translate("DialogNewPass", "New password:", None, -1))

