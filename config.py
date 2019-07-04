# -*- coding: utf-8 -*-
"""
.. module:: config
    :platform: Linux, Windows
    :synopsis: config variables

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>

Variables set:

    :fontname: monospace font used in calculation results widgets
    :fontsize: font size used in calculation results widgets
    :homedir: start dir used for loading fieldbooks
    :template_dir: path to template files for batch plotting
    :log_path: path to log file
    :line_tolerance: snapping tolerance to line tool
    :area_tolerance: area tolerance for area division
    :max_iteration: maximal number of iterations for area division
    :gama_path: full path to gama-local, default plug-in dir
"""
from qgis.PyQt.QtCore import QDir, QFileInfo, QSettings
from qgis.core import QgsProject

# dialogs
fontname = 'DejaVu Sans Mono'
fontsize = 9
#
homedir = QDir().cleanPath(QFileInfo(__file__).absolutePath())
# plot template
template_dir = QDir(homedir).absoluteFilePath("template")
# logging
log_path = '/tmp/log.log'
# line tool
line_tolerance = 1.0  # tolerance in layer units
# area division
area_tolerance = 0.5  # tolerance in layer units
max_iteration = 100  # maximum number of iteration in area division
# GNU Gama - full path to gama-local
gama_path = '/home/siki/Downloads/gama-1.15/bin/gama-local'
# Config for preferred distance and angle units (stored and displayed). These are combo box indexes.
distance_stored = 0
distance_displayed = 0
angle_stored = 0
angle_displayed = 0


def store_config():
    proj = QgsProject.instance()
    global fontname, fontsize, homedir, log_path, gama_path, template_dir, line_tolerance, area_tolerance
    global max_iteration, distance_stored, distance_displayed, angle_stored, angle_displayed

    QSettings().setValue('SurveyingCalculation/fontname', fontname)
    QSettings().setValue('SurveyingCalculation/fontsize', fontsize)
    QSettings().setValue('SurveyingCalculation/homedir', homedir)
    QSettings().setValue('SurveyingCalculation/log_path', log_path)
    QSettings().setValue('SurveyingCalculation/gama_path', gama_path)
    QSettings().setValue('SurveyingCalculation/template_dir', template_dir)
    QSettings().sync()

    proj.writeEntry('SurveyingCalculation', 'distanceUnitsStored', distance_stored)
    proj.writeEntry('SurveyingCalculation', 'distanceUnitsDisplayed', distance_displayed)
    proj.writeEntry('SurveyingCalculation', 'angleUnitsStored', angle_stored)
    proj.writeEntry('SurveyingCalculation', 'angleUnitsDisplayed', angle_displayed)
    proj.writeEntryDouble('SurveyingCalculation', 'lineTolerance', line_tolerance)
    proj.writeEntryDouble('SurveyingCalculation', 'areaTolerance', area_tolerance)
    proj.writeEntryDouble('SurveyingCalculation', 'maxIteration', max_iteration)


def load_config():
    proj = QgsProject.instance()

    global fontname, fontsize, homedir, log_path, gama_path, template_dir, line_tolerance, area_tolerance
    global max_iteration, distance_stored, distance_displayed, angle_stored, angle_displayed

    fontname = QSettings().value("SurveyingCalculation/fontname", fontname)
    fontsize = int(QSettings().value("SurveyingCalculation/fontsize", fontsize))
    homedir = QSettings().value("SurveyingCalculation/homedir", homedir)
    log_path = QSettings().value("SurveyingCalculation/log_path", log_path)
    gama_path = QSettings().value("SurveyingCalculation/gama_path", gama_path)
    template_dir = QSettings().value("SurveyingCalculation/template_dir", template_dir)
    line_tolerance, _ = proj.readDoubleEntry('SurveyingCalculation', 'lineTolerance', line_tolerance)
    area_tolerance, _ = proj.readDoubleEntry('SurveyingCalculation', 'areaTolerance', area_tolerance)
    max_iteration, _ = proj.readNumEntry('SurveyingCalculation', 'maxIteration', max_iteration)
    distance_stored, _ = proj.readNumEntry('SurveyingCalculation', 'distanceUnitsStored', distance_stored)
    distance_displayed, _ = proj.readNumEntry('SurveyingCalculation', 'distanceUnitsDisplayed', distance_displayed)
    angle_stored, _ = proj.readNumEntry('SurveyingCalculation', 'angleUnitsStored', angle_stored)
    angle_displayed, _ = proj.readNumEntry('SurveyingCalculation', 'angleUnitsDisplayed', angle_displayed)
