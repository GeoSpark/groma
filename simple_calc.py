# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_calc.ui'
#
# Created: Tue Nov 18 18:27:09 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SimpleCalcDialog(object):
    def setupUi(self, SimpleCalcDialog):
        SimpleCalcDialog.setObjectName(_fromUtf8("SimpleCalcDialog"))
        SimpleCalcDialog.resize(720, 463)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SimpleCalcDialog.sizePolicy().hasHeightForWidth())
        SimpleCalcDialog.setSizePolicy(sizePolicy)
        SimpleCalcDialog.setMinimumSize(QtCore.QSize(720, 463))
        SimpleCalcDialog.setMaximumSize(QtCore.QSize(720, 463))
        self.RadioGroup = QtGui.QGroupBox(SimpleCalcDialog)
        self.RadioGroup.setGeometry(QtCore.QRect(10, 10, 141, 191))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RadioGroup.sizePolicy().hasHeightForWidth())
        self.RadioGroup.setSizePolicy(sizePolicy)
        self.RadioGroup.setFlat(False)
        self.RadioGroup.setCheckable(False)
        self.RadioGroup.setObjectName(_fromUtf8("RadioGroup"))
        self.OrientRadio = QtGui.QRadioButton(self.RadioGroup)
        self.OrientRadio.setGeometry(QtCore.QRect(10, 30, 151, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OrientRadio.sizePolicy().hasHeightForWidth())
        self.OrientRadio.setSizePolicy(sizePolicy)
        self.OrientRadio.setObjectName(_fromUtf8("OrientRadio"))
        self.radioButtonGroup = QtGui.QButtonGroup(SimpleCalcDialog)
        self.radioButtonGroup.setObjectName(_fromUtf8("radioButtonGroup"))
        self.radioButtonGroup.addButton(self.OrientRadio)
        self.RadialRadio = QtGui.QRadioButton(self.RadioGroup)
        self.RadialRadio.setGeometry(QtCore.QRect(10, 60, 161, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RadialRadio.sizePolicy().hasHeightForWidth())
        self.RadialRadio.setSizePolicy(sizePolicy)
        self.RadialRadio.setObjectName(_fromUtf8("RadialRadio"))
        self.radioButtonGroup.addButton(self.RadialRadio)
        self.IntersectRadio = QtGui.QRadioButton(self.RadioGroup)
        self.IntersectRadio.setGeometry(QtCore.QRect(10, 90, 151, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IntersectRadio.sizePolicy().hasHeightForWidth())
        self.IntersectRadio.setSizePolicy(sizePolicy)
        self.IntersectRadio.setObjectName(_fromUtf8("IntersectRadio"))
        self.radioButtonGroup.addButton(self.IntersectRadio)
        self.ResectionRadio = QtGui.QRadioButton(self.RadioGroup)
        self.ResectionRadio.setGeometry(QtCore.QRect(10, 120, 141, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResectionRadio.sizePolicy().hasHeightForWidth())
        self.ResectionRadio.setSizePolicy(sizePolicy)
        self.ResectionRadio.setObjectName(_fromUtf8("ResectionRadio"))
        self.radioButtonGroup.addButton(self.ResectionRadio)
        self.FreeRadio = QtGui.QRadioButton(self.RadioGroup)
        self.FreeRadio.setGeometry(QtCore.QRect(10, 150, 141, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FreeRadio.sizePolicy().hasHeightForWidth())
        self.FreeRadio.setSizePolicy(sizePolicy)
        self.FreeRadio.setObjectName(_fromUtf8("FreeRadio"))
        self.radioButtonGroup.addButton(self.FreeRadio)
        self.PointsGroup = QtGui.QGroupBox(SimpleCalcDialog)
        self.PointsGroup.setGeometry(QtCore.QRect(330, 10, 381, 191))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PointsGroup.sizePolicy().hasHeightForWidth())
        self.PointsGroup.setSizePolicy(sizePolicy)
        self.PointsGroup.setObjectName(_fromUtf8("PointsGroup"))
        self.AddButton = QtGui.QPushButton(self.PointsGroup)
        self.AddButton.setGeometry(QtCore.QRect(150, 50, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddButton.sizePolicy().hasHeightForWidth())
        self.AddButton.setSizePolicy(sizePolicy)
        self.AddButton.setObjectName(_fromUtf8("AddButton"))
        self.AddAllButton = QtGui.QPushButton(self.PointsGroup)
        self.AddAllButton.setGeometry(QtCore.QRect(150, 80, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddAllButton.sizePolicy().hasHeightForWidth())
        self.AddAllButton.setSizePolicy(sizePolicy)
        self.AddAllButton.setObjectName(_fromUtf8("AddAllButton"))
        self.RemoveButton = QtGui.QPushButton(self.PointsGroup)
        self.RemoveButton.setGeometry(QtCore.QRect(150, 120, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RemoveButton.sizePolicy().hasHeightForWidth())
        self.RemoveButton.setSizePolicy(sizePolicy)
        self.RemoveButton.setObjectName(_fromUtf8("RemoveButton"))
        self.RemoveAllButton = QtGui.QPushButton(self.PointsGroup)
        self.RemoveAllButton.setGeometry(QtCore.QRect(150, 150, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RemoveAllButton.sizePolicy().hasHeightForWidth())
        self.RemoveAllButton.setSizePolicy(sizePolicy)
        self.RemoveAllButton.setObjectName(_fromUtf8("RemoveAllButton"))
        self.TargetPointsLabel = QtGui.QLabel(self.PointsGroup)
        self.TargetPointsLabel.setGeometry(QtCore.QRect(10, 20, 121, 16))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TargetPointsLabel.sizePolicy().hasHeightForWidth())
        self.TargetPointsLabel.setSizePolicy(sizePolicy)
        self.TargetPointsLabel.setObjectName(_fromUtf8("TargetPointsLabel"))
        self.UsedPointsLabel = QtGui.QLabel(self.PointsGroup)
        self.UsedPointsLabel.setGeometry(QtCore.QRect(250, 20, 121, 16))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UsedPointsLabel.sizePolicy().hasHeightForWidth())
        self.UsedPointsLabel.setSizePolicy(sizePolicy)
        self.UsedPointsLabel.setObjectName(_fromUtf8("UsedPointsLabel"))
        self.SourceList = QtGui.QListWidget(self.PointsGroup)
        self.SourceList.setGeometry(QtCore.QRect(10, 40, 121, 141))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SourceList.sizePolicy().hasHeightForWidth())
        self.SourceList.setSizePolicy(sizePolicy)
        self.SourceList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.SourceList.setObjectName(_fromUtf8("SourceList"))
        self.TargetList = QtGui.QListWidget(self.PointsGroup)
        self.TargetList.setGeometry(QtCore.QRect(250, 40, 121, 141))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TargetList.sizePolicy().hasHeightForWidth())
        self.TargetList.setSizePolicy(sizePolicy)
        self.TargetList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.TargetList.setObjectName(_fromUtf8("TargetList"))
        self.ResultGroup = QtGui.QGroupBox(SimpleCalcDialog)
        self.ResultGroup.setGeometry(QtCore.QRect(10, 210, 701, 201))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResultGroup.sizePolicy().hasHeightForWidth())
        self.ResultGroup.setSizePolicy(sizePolicy)
        self.ResultGroup.setObjectName(_fromUtf8("ResultGroup"))
        self.ResultTextBrowser = QtGui.QTextBrowser(self.ResultGroup)
        self.ResultTextBrowser.setGeometry(QtCore.QRect(10, 20, 681, 171))
        self.ResultTextBrowser.setObjectName(_fromUtf8("ResultTextBrowser"))
        self.StationGroup = QtGui.QGroupBox(SimpleCalcDialog)
        self.StationGroup.setGeometry(QtCore.QRect(170, 10, 141, 191))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StationGroup.sizePolicy().hasHeightForWidth())
        self.StationGroup.setSizePolicy(sizePolicy)
        self.StationGroup.setObjectName(_fromUtf8("StationGroup"))
        self.Station1Combo = QtGui.QComboBox(self.StationGroup)
        self.Station1Combo.setGeometry(QtCore.QRect(10, 50, 121, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Station1Combo.sizePolicy().hasHeightForWidth())
        self.Station1Combo.setSizePolicy(sizePolicy)
        self.Station1Combo.setObjectName(_fromUtf8("Station1Combo"))
        self.Station1Label = QtGui.QLabel(self.StationGroup)
        self.Station1Label.setGeometry(QtCore.QRect(10, 20, 121, 16))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Station1Label.sizePolicy().hasHeightForWidth())
        self.Station1Label.setSizePolicy(sizePolicy)
        self.Station1Label.setObjectName(_fromUtf8("Station1Label"))
        self.Station2Label = QtGui.QLabel(self.StationGroup)
        self.Station2Label.setGeometry(QtCore.QRect(10, 90, 111, 16))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Station2Label.sizePolicy().hasHeightForWidth())
        self.Station2Label.setSizePolicy(sizePolicy)
        self.Station2Label.setObjectName(_fromUtf8("Station2Label"))
        self.Station2Combo = QtGui.QComboBox(self.StationGroup)
        self.Station2Combo.setGeometry(QtCore.QRect(10, 120, 121, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Station2Combo.sizePolicy().hasHeightForWidth())
        self.Station2Combo.setSizePolicy(sizePolicy)
        self.Station2Combo.setObjectName(_fromUtf8("Station2Combo"))
        self.CalcButton = QtGui.QPushButton(SimpleCalcDialog)
        self.CalcButton.setGeometry(QtCore.QRect(420, 430, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CalcButton.sizePolicy().hasHeightForWidth())
        self.CalcButton.setSizePolicy(sizePolicy)
        self.CalcButton.setObjectName(_fromUtf8("CalcButton"))
        self.HelpButton = QtGui.QPushButton(SimpleCalcDialog)
        self.HelpButton.setGeometry(QtCore.QRect(20, 430, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HelpButton.sizePolicy().hasHeightForWidth())
        self.HelpButton.setSizePolicy(sizePolicy)
        self.HelpButton.setObjectName(_fromUtf8("HelpButton"))
        self.ResetButton = QtGui.QPushButton(SimpleCalcDialog)
        self.ResetButton.setGeometry(QtCore.QRect(520, 430, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResetButton.sizePolicy().hasHeightForWidth())
        self.ResetButton.setSizePolicy(sizePolicy)
        self.ResetButton.setObjectName(_fromUtf8("ResetButton"))
        self.CloseButton = QtGui.QPushButton(SimpleCalcDialog)
        self.CloseButton.setGeometry(QtCore.QRect(620, 430, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CloseButton.sizePolicy().hasHeightForWidth())
        self.CloseButton.setSizePolicy(sizePolicy)
        self.CloseButton.setObjectName(_fromUtf8("CloseButton"))

        self.retranslateUi(SimpleCalcDialog)
        QtCore.QMetaObject.connectSlotsByName(SimpleCalcDialog)
        SimpleCalcDialog.setTabOrder(self.OrientRadio, self.RadialRadio)
        SimpleCalcDialog.setTabOrder(self.RadialRadio, self.IntersectRadio)
        SimpleCalcDialog.setTabOrder(self.IntersectRadio, self.ResectionRadio)
        SimpleCalcDialog.setTabOrder(self.ResectionRadio, self.FreeRadio)
        SimpleCalcDialog.setTabOrder(self.FreeRadio, self.Station1Combo)
        SimpleCalcDialog.setTabOrder(self.Station1Combo, self.Station2Combo)
        SimpleCalcDialog.setTabOrder(self.Station2Combo, self.AddButton)
        SimpleCalcDialog.setTabOrder(self.AddButton, self.AddAllButton)
        SimpleCalcDialog.setTabOrder(self.AddAllButton, self.RemoveButton)
        SimpleCalcDialog.setTabOrder(self.RemoveButton, self.RemoveAllButton)
        SimpleCalcDialog.setTabOrder(self.RemoveAllButton, self.HelpButton)
        SimpleCalcDialog.setTabOrder(self.HelpButton, self.CalcButton)
        SimpleCalcDialog.setTabOrder(self.CalcButton, self.ResetButton)
        SimpleCalcDialog.setTabOrder(self.ResetButton, self.CloseButton)

    def retranslateUi(self, SimpleCalcDialog):
        SimpleCalcDialog.setWindowTitle(_translate("SimpleCalcDialog", "Simple Point Calculations", None))
        self.RadioGroup.setTitle(_translate("SimpleCalcDialog", "Calculation", None))
        self.OrientRadio.setToolTip(_translate("SimpleCalcDialog", "Calculate orientation angle  on stations", None))
        self.OrientRadio.setText(_translate("SimpleCalcDialog", "Orientation", None))
        self.RadialRadio.setText(_translate("SimpleCalcDialog", "Radial Survey", None))
        self.IntersectRadio.setText(_translate("SimpleCalcDialog", "Intersection", None))
        self.ResectionRadio.setText(_translate("SimpleCalcDialog", "Resection", None))
        self.FreeRadio.setText(_translate("SimpleCalcDialog", "Free Station", None))
        self.PointsGroup.setTitle(_translate("SimpleCalcDialog", "Points", None))
        self.AddButton.setText(_translate("SimpleCalcDialog", "Add >", None))
        self.AddAllButton.setText(_translate("SimpleCalcDialog", "Add all", None))
        self.RemoveButton.setText(_translate("SimpleCalcDialog", "< Remove", None))
        self.RemoveAllButton.setText(_translate("SimpleCalcDialog", "Remove all", None))
        self.TargetPointsLabel.setText(_translate("SimpleCalcDialog", "Target Points", None))
        self.UsedPointsLabel.setText(_translate("SimpleCalcDialog", "Used Points", None))
        self.ResultGroup.setTitle(_translate("SimpleCalcDialog", "Result of Calculations", None))
        self.StationGroup.setTitle(_translate("SimpleCalcDialog", "Station", None))
        self.Station1Label.setText(_translate("SimpleCalcDialog", "Station (1)", None))
        self.Station2Label.setText(_translate("SimpleCalcDialog", "Station (2)", None))
        self.CalcButton.setText(_translate("SimpleCalcDialog", "Calculate", None))
        self.HelpButton.setText(_translate("SimpleCalcDialog", "Help", None))
        self.ResetButton.setText(_translate("SimpleCalcDialog", "Reset", None))
        self.CloseButton.setText(_translate("SimpleCalcDialog", "Close", None))

