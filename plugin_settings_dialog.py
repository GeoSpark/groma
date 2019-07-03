# -*- coding: utf-8 -*-
"""
.. module:: plugin_settings_dialog
    :platform: Linux, Windows
    :synopsis: GUI for SurveyingCalculation plugin settings

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
from __future__ import absolute_import
from builtins import range
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QMessageBox
from qgis.PyQt.QtCore import Qt
from . import config
from .plugin_settings import Ui_PluginSettingsDialog
from .base_classes import tr


class PluginSettingsDialog(QDialog):
    """ Class for plugin settings dialog
    """

    def __init__(self):
        """ Initialize dialog data and event handlers
        """
        super(PluginSettingsDialog, self).__init__()
        self.ui = Ui_PluginSettingsDialog()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        # event handlers
        self.ui.HomeDirButton.clicked.connect(self.onHomeDirButton)
        self.ui.LogPathButton.clicked.connect(self.onLogPathButton)
        self.ui.GamaPathButton.clicked.connect(self.onGamaPathButton)
        self.ui.PlotTemplateDirButton.clicked.connect(self.onPlotTemplateDirButton)
        self.ui.OKButton.clicked.connect(self.onOKButton)
        self.ui.CancelButton.clicked.connect(self.onCancelButton)

        self.fillWidgets()

    def fillWidgets(self):
        """ Fill all widgets of Plugins Settings dialog.
        """
        for i in range(8, 20):
            self.ui.FontSizeCombo.addItem("%d" % i)

        config.load_config()

        self.ui.FontNameCombo.setCurrentIndex(self.ui.FontNameCombo.findText(config.fontname))
        self.ui.FontSizeCombo.setCurrentIndex(self.ui.FontSizeCombo.findText("%d" % config.fontsize))
        self.ui.HomeDirEdit.setText(config.homedir)
        self.ui.LogPathEdit.setText(config.log_path)
        self.ui.GamaPathEdit.setText(config.gama_path)
        self.ui.PlotTemplateDirEdit.setText(config.template_dir)
        self.ui.LineToleranceEdit.setText(str(config.line_tolerance))
        self.ui.AreaToleranceEdit.setText(str(config.area_tolerance))
        self.ui.MaxIterationEdit.setText(str(config.max_iteration))
        self.ui.comboDistanceStore.setCurrentIndex(config.distance_stored)
        self.ui.comboDistanceStore.setCurrentIndex(config.distance_displayed)
        self.ui.comboDistanceStore.setCurrentIndex(config.angle_stored)
        self.ui.comboDistanceStore.setCurrentIndex(config.angle_displayed)

    def onHomeDirButton(self):
        """ Change the home directory where fieldbooks are stored.
        """
        path = QFileDialog.getExistingDirectory(self,
                                                tr("Select Home Directory"),
                                                self.ui.HomeDirEdit.text(),
                                                QFileDialog.ShowDirsOnly)
        if path != "":
            self.ui.HomeDirEdit.setText(path)

    def onLogPathButton(self):
        """ Change the directory of the log file.
        """
        path, __ = QFileDialog.getSaveFileName(self,
                                               tr("Select Log File Path"),
                                               self.ui.LogPathEdit.text(), "", "",
                                               QFileDialog.DontConfirmOverwrite)
        if path != "":
            self.ui.LogPathEdit.setText(path)

    def onGamaPathButton(self):
        """ Change the directory of the gama-local executable.
        """
        path, __ = QFileDialog.getOpenFileName(self,
                                               tr("Select Path to GNU Gama Executable"),
                                               self.ui.GamaPathEdit.text())
        if path != "":
            self.ui.GamaPathEdit.setText(path)

    def onPlotTemplateDirButton(self):
        """ Change the directory of the plot template files.
        """
        path = QFileDialog.getExistingDirectory(self,
                                                tr("Select Plot Template Directory"),
                                                self.ui.PlotTemplateDirEdit.text(),
                                                QFileDialog.ShowDirsOnly)
        if path != "":
            self.ui.PlotTemplateDirEdit.setText(path)

    def onOKButton(self):
        """ Close dialog. The changes will be saved.
        """
        # check values in widgets
        try:
            line_tolerance = float(self.ui.LineToleranceEdit.text())
        except ValueError:
            QMessageBox.warning(self, tr("Warning"),
                                tr("Snap tolerance must be a positive float value in layer units!"))
            self.ui.LineToleranceEdit.setFocus()
            return
        if line_tolerance <= 0.0:
            QMessageBox.warning(self, tr("Warning"),
                                tr("Snap tolerance must be a positive float value in layer units!"))
            self.ui.LineToleranceEdit.setFocus()
            return
        try:
            area_tolerance = float(self.ui.AreaToleranceEdit.text())
        except ValueError:
            QMessageBox.warning(self, tr("Warning"),
                                tr("Area tolerance must be a positive float value in layer units!"))
            self.ui.AreaToleranceEdit.setFocus()
            return
        if area_tolerance <= 0.0:
            QMessageBox.warning(self, tr("Warning"),
                                tr("Area tolerance must be a positive float value in layer units!"))
            self.ui.AreaToleranceEdit.setFocus()
            return
        try:
            max_iteration = int(self.ui.MaxIterationEdit.text())
        except ValueError:
            QMessageBox.warning(self, tr("Warning"), tr("Maximum iteration must be a positive integer value!"))
            self.ui.MaxIterationEdit.setFocus()
            return
        if max_iteration <= 0:
            QMessageBox.warning(self, tr("Warning"), tr("Maximum iteration must be a positive integer value!"))
            self.ui.MaxIterationEdit.setFocus()
            return

        config.fontname = self.ui.FontNameCombo.currentText()
        config.fontsize = self.ui.FontSizeCombo.currentText()
        config.homedir = self.ui.HomeDirEdit.text()
        config.log_path = self.ui.LogPathEdit.text()
        config.gama_path = self.ui.GamaPathEdit.text()
        config.template_dir = self.ui.PlotTemplateDirEdit.text()
        config.distance_stored = self.ui.comboDistanceStore.currentIndex()
        config.distance_displayed = self.ui.comboDistanceDisplay.currentIndex()
        config.angle_stored = self.ui.comboAngleStore.currentIndex()
        config.angle_displayed = self.ui.comboAngleDisplay.currentIndex()
        config.line_tolerance = line_tolerance
        config.area_tolerance = area_tolerance
        config.max_iteration = max_iteration
        config.store_config()

        self.accept()

    def onCancelButton(self):
        """ Cancel dialog. The changes won't be saved.
        """
        self.reject()
