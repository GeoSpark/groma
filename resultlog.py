#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: resultlog
    :platform: Linux, Windows
    :synopsis: main module

.. moduleauthor:: Zoltan Siki <siki@agt.bme.hu>
"""
import logging

from qgis.PyQt.QtCore import QDir
from qgis.core import Qgis, QgsMessageLog


class ResultLog(object):
    """ File based logging for Surveying Calculations. Events & calculation results are logged into this file.
    """
    resultlog_message = ""

    def __init__(self, logfile):
        """ initialize log file if the given file cannot be opened for output then a SurveyingCalculation.log file in the temperary directory will be used

            :param logfile: name of the log file it will be created if neccessary, messages will be appended to the end
        """
        self.logfile = self.set_log_path(logfile)
        QgsMessageLog.logMessage(f'Log file set to {self.logfile}', 'SurveyingCalculation', level=Qgis.Info)

    def set_log_path(self, log_path):
        log_path = QDir.temp().absoluteFilePath(log_path)
        logging.basicConfig(filename=log_path, level=logging.DEBUG)
        return log_path

    def reset(self):
        """ Delete content of log file
        """
        pass

    def write(self, msg=""):
        """ Write a  simple message to log

            :param msg: message to write
        """
        self.write_log(msg)

    def write_log(self, msg):
        """ Write log message with date & time

            :param msg: message to write
        """
        logging.info(msg)
        QgsMessageLog.logMessage(msg, 'SurveyingCalculation', level=Qgis.Info)
