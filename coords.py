# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coords.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CoordDialog(object):
    def setupUi(self, CoordDialog):
        CoordDialog.setObjectName("CoordDialog")
        CoordDialog.resize(320, 172)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CoordDialog.sizePolicy().hasHeightForWidth())
        CoordDialog.setSizePolicy(sizePolicy)
        CoordDialog.setMinimumSize(QtCore.QSize(320, 172))
        CoordDialog.setMaximumSize(QtCore.QSize(320, 172))
        CoordDialog.setAccessibleName("")
        CoordDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.ContinueButton = QtWidgets.QPushButton(CoordDialog)
        self.ContinueButton.setGeometry(QtCore.QRect(120, 140, 81, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ContinueButton.sizePolicy().hasHeightForWidth())
        self.ContinueButton.setSizePolicy(sizePolicy)
        self.ContinueButton.setObjectName("ContinueButton")
        self.CancelButton = QtWidgets.QPushButton(CoordDialog)
        self.CancelButton.setGeometry(QtCore.QRect(220, 140, 81, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CancelButton.sizePolicy().hasHeightForWidth())
        self.CancelButton.setSizePolicy(sizePolicy)
        self.CancelButton.setObjectName("CancelButton")
        self.DivLineGroup = QtWidgets.QGroupBox(CoordDialog)
        self.DivLineGroup.setGeometry(QtCore.QRect(10, 10, 301, 121))
        self.DivLineGroup.setObjectName("DivLineGroup")
        self.StartEast = QtWidgets.QLineEdit(self.DivLineGroup)
        self.StartEast.setGeometry(QtCore.QRect(170, 20, 121, 20))
        self.StartEast.setMaxLength(32)
        self.StartEast.setObjectName("StartEast")
        self.StartEastLabel = QtWidgets.QLabel(self.DivLineGroup)
        self.StartEastLabel.setGeometry(QtCore.QRect(10, 20, 151, 16))
        self.StartEastLabel.setObjectName("StartEastLabel")
        self.StartNorthLabel = QtWidgets.QLabel(self.DivLineGroup)
        self.StartNorthLabel.setGeometry(QtCore.QRect(10, 40, 151, 16))
        self.StartNorthLabel.setObjectName("StartNorthLabel")
        self.StartNorth = QtWidgets.QLineEdit(self.DivLineGroup)
        self.StartNorth.setGeometry(QtCore.QRect(170, 40, 121, 20))
        self.StartNorth.setMaxLength(32)
        self.StartNorth.setReadOnly(False)
        self.StartNorth.setObjectName("StartNorth")
        self.EndNorthLabel = QtWidgets.QLabel(self.DivLineGroup)
        self.EndNorthLabel.setGeometry(QtCore.QRect(10, 90, 151, 16))
        self.EndNorthLabel.setObjectName("EndNorthLabel")
        self.EndEast = QtWidgets.QLineEdit(self.DivLineGroup)
        self.EndEast.setGeometry(QtCore.QRect(170, 70, 121, 20))
        self.EndEast.setMaxLength(32)
        self.EndEast.setObjectName("EndEast")
        self.EndNorth = QtWidgets.QLineEdit(self.DivLineGroup)
        self.EndNorth.setGeometry(QtCore.QRect(170, 90, 120, 20))
        self.EndNorth.setMaxLength(32)
        self.EndNorth.setReadOnly(False)
        self.EndNorth.setObjectName("EndNorth")
        self.EndEastLabel = QtWidgets.QLabel(self.DivLineGroup)
        self.EndEastLabel.setGeometry(QtCore.QRect(10, 70, 151, 16))
        self.EndEastLabel.setObjectName("EndEastLabel")

        self.retranslateUi(CoordDialog)
        QtCore.QMetaObject.connectSlotsByName(CoordDialog)
        CoordDialog.setTabOrder(self.StartEast, self.ContinueButton)
        CoordDialog.setTabOrder(self.ContinueButton, self.CancelButton)

    def retranslateUi(self, CoordDialog):
        _translate = QtCore.QCoreApplication.translate
        CoordDialog.setWindowTitle(_translate("CoordDialog", "Area Division"))
        self.ContinueButton.setText(_translate("CoordDialog", "Continue"))
        self.CancelButton.setText(_translate("CoordDialog", "Cancel"))
        self.DivLineGroup.setTitle(_translate("CoordDialog", "Division line"))
        self.StartEastLabel.setText(_translate("CoordDialog", "Start point east"))
        self.StartNorthLabel.setText(_translate("CoordDialog", "Start point north"))
        self.EndNorthLabel.setText(_translate("CoordDialog", "End point north"))
        self.EndEastLabel.setText(_translate("CoordDialog", "End point east"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CoordDialog = QtWidgets.QDialog()
    ui = Ui_CoordDialog()
    ui.setupUi(CoordDialog)
    CoordDialog.show()
    sys.exit(app.exec_())

