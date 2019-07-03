# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'area_div.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AreaDivDialog(object):
    def setupUi(self, AreaDivDialog):
        AreaDivDialog.setObjectName("AreaDivDialog")
        AreaDivDialog.resize(320, 172)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AreaDivDialog.sizePolicy().hasHeightForWidth())
        AreaDivDialog.setSizePolicy(sizePolicy)
        AreaDivDialog.setMinimumSize(QtCore.QSize(320, 172))
        AreaDivDialog.setMaximumSize(QtCore.QSize(320, 172))
        AreaDivDialog.setAccessibleName("")
        AreaDivDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.DivideButton = QtWidgets.QPushButton(AreaDivDialog)
        self.DivideButton.setGeometry(QtCore.QRect(120, 140, 81, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DivideButton.sizePolicy().hasHeightForWidth())
        self.DivideButton.setSizePolicy(sizePolicy)
        self.DivideButton.setObjectName("DivideButton")
        self.CancelButton = QtWidgets.QPushButton(AreaDivDialog)
        self.CancelButton.setGeometry(QtCore.QRect(220, 140, 81, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CancelButton.sizePolicy().hasHeightForWidth())
        self.CancelButton.setSizePolicy(sizePolicy)
        self.CancelButton.setObjectName("CancelButton")
        self.AreaDivGroup = QtWidgets.QGroupBox(AreaDivDialog)
        self.AreaDivGroup.setGeometry(QtCore.QRect(10, 10, 301, 121))
        self.AreaDivGroup.setObjectName("AreaDivGroup")
        self.AreaLineEdit = QtWidgets.QLineEdit(self.AreaDivGroup)
        self.AreaLineEdit.setGeometry(QtCore.QRect(170, 20, 121, 20))
        self.AreaLineEdit.setObjectName("AreaLineEdit")
        self.AreaLabel = QtWidgets.QLabel(self.AreaDivGroup)
        self.AreaLabel.setGeometry(QtCore.QRect(10, 20, 151, 16))
        self.AreaLabel.setObjectName("AreaLabel")
        self.OnePointRadio = QtWidgets.QRadioButton(self.AreaDivGroup)
        self.OnePointRadio.setGeometry(QtCore.QRect(10, 90, 271, 17))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OnePointRadio.sizePolicy().hasHeightForWidth())
        self.OnePointRadio.setSizePolicy(sizePolicy)
        self.OnePointRadio.setObjectName("OnePointRadio")
        self.TwoPointRadio = QtWidgets.QRadioButton(self.AreaDivGroup)
        self.TwoPointRadio.setGeometry(QtCore.QRect(10, 70, 271, 17))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TwoPointRadio.sizePolicy().hasHeightForWidth())
        self.TwoPointRadio.setSizePolicy(sizePolicy)
        self.TwoPointRadio.setObjectName("TwoPointRadio")
        self.TotalLabel = QtWidgets.QLabel(self.AreaDivGroup)
        self.TotalLabel.setGeometry(QtCore.QRect(10, 40, 151, 16))
        self.TotalLabel.setObjectName("TotalLabel")
        self.TotalLineEdit = QtWidgets.QLineEdit(self.AreaDivGroup)
        self.TotalLineEdit.setGeometry(QtCore.QRect(170, 40, 121, 20))
        self.TotalLineEdit.setReadOnly(True)
        self.TotalLineEdit.setObjectName("TotalLineEdit")

        self.retranslateUi(AreaDivDialog)
        QtCore.QMetaObject.connectSlotsByName(AreaDivDialog)
        AreaDivDialog.setTabOrder(self.AreaLineEdit, self.OnePointRadio)
        AreaDivDialog.setTabOrder(self.OnePointRadio, self.TwoPointRadio)
        AreaDivDialog.setTabOrder(self.TwoPointRadio, self.DivideButton)
        AreaDivDialog.setTabOrder(self.DivideButton, self.CancelButton)

    def retranslateUi(self, AreaDivDialog):
        _translate = QtCore.QCoreApplication.translate
        AreaDivDialog.setWindowTitle(_translate("AreaDivDialog", "Area Division"))
        self.DivideButton.setText(_translate("AreaDivDialog", "Divide"))
        self.CancelButton.setText(_translate("AreaDivDialog", "Cancel"))
        self.AreaDivGroup.setTitle(_translate("AreaDivDialog", "Divide selected area"))
        self.AreaLabel.setText(_translate("AreaDivDialog", "Area (in layer units)"))
        self.OnePointRadio.setText(_translate("AreaDivDialog", "Through the first given point"))
        self.TwoPointRadio.setText(_translate("AreaDivDialog", "Parallel to the given line"))
        self.TotalLabel.setText(_translate("AreaDivDialog", "Full area"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AreaDivDialog = QtWidgets.QDialog()
    ui = Ui_AreaDivDialog()
    ui.setupUi(AreaDivDialog)
    AreaDivDialog.show()
    sys.exit(app.exec_())

