# -*- coding: utf-8 -*-
"""
.. module:: surveying_calculation
    :platform: Linux, Windows
    :synopsis: main module

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>

"""
import webbrowser

from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo, QRegExp, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu, QMessageBox, QFileDialog, QDialog
# noinspection PyUnresolvedReferences
from qgis.core import Qgis, QgsMessageLog, QgsMapLayer, QgsWkbTypes, QgsVectorLayer

# plugin specific python modules
from .line_tool import LineMapTool
from .network_dialog import NetworkDialog
from .new_point_dialog import NewPointDialog
# from .batch_plotting_dialog import BatchPlottingDialog
from .plugin_settings_dialog import PluginSettingsDialog
from .resultlog import *
from .single_dialog import SingleDialog
from .surveying_util import *
from .totalstations import *
from .transformation_dialog import TransformationDialog
from .traverse_dialog import TraverseDialog


# noinspection PyUnresolvedReferences
class SurveyingCalculation(object):
    """SurveyingCalculation QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: an interface instance that will be passed to this class which provides the hook by which you can
        manipulate the QGIS application at run time (QgsInterface)
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = QDir().cleanPath(QFileInfo(__file__).absolutePath())
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = QDir.cleanPath(self.plugin_dir + QDir.separator() + 'i18n' +
                                     QDir.separator() + '{}.qm'.format(locale))
        if QFileInfo(locale_path).exists():
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # init result log
        log_path_2 = config.log_path

        if len(log_path_2) > 0:
            log_path = log_path_2
        else:
            log_path = QDir.cleanPath(self.plugin_dir + QDir.separator() + 'log' +
                                      QDir.separator() + 'log.txt')
        self.log = ResultLog(log_path)

        self.newp_dlg = NewPointDialog()
        self.single_dlg = SingleDialog(self.log)
        self.traverse_dlg = TraverseDialog(self.log)
        self.network_dlg = NetworkDialog(self.log)
        self.transformation_dlg = TransformationDialog(self.log)
        # self.plotbytemplate_dlg = BatchPlottingDialog(self.iface, False)
        # self.batchplotting_dlg = BatchPlottingDialog(self.iface, True)

        config.load_config()

        QgsMessageLog.logMessage('Plugin initialised', 'SurveyingCalculation', level=Qgis.Info)

    def add_action(self, icon_path, text, callback, enabled_flag=True,
                   add_to_menu=True, add_to_toolbar=True, status_tip=None,
                   whats_this=None, parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.

        :param icon_path: path to the icon for this action. Can be a resource path (e.g. ':/plugins/foo/bar.png') or a
                          normal file system path (str)
        :param text: text that should be shown in menu items for this action (str)
        :param callback: function to be called when the action is triggered (function)
        :param enabled_flag: a flag indicating if the action should be enabled by default (bool). Defaults to True.
        :param add_to_menu: flag indicating whether the action should also be added to the menu (bool).
                            Defaults to True.
        :param add_to_toolbar: flag indicating whether the action should also be added to the toolbar (bool).
                               Defaults to True.
        :param status_tip: optional text to show in a popup when mouse pointer hovers over the action (str)
        :param parent: parent widget for the new action (QWidget). Defaults None.
        :param whats_this: optional text to show in the status bar when the mouse pointer hovers over the action (str)
        :returns: the action that was created (Qaction). Note that the action is also added to self.actions list.
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)
        self.actions.append(action)
        return action

    # noinspection PyAttributeOutsideInit
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_dir = QDir.cleanPath(self.plugin_dir + QDir.separator() + 'icons')
        # build menu
        self.actions = []
        self.menu = QMenu()
        self.menu.setTitle(tr(u'&SurveyingCalculation'))
        self.sc_coord = QAction(QIcon(QDir(icon_dir).absoluteFilePath('new_coord.png')), tr("New coordinate list ..."),
                                self.iface.mainWindow())
        self.sc_fb = QAction(QIcon(QDir(icon_dir).absoluteFilePath('new_fb.png')), tr("New fieldbook ..."),
                             self.iface.mainWindow())
        self.sc_load = QAction(QIcon(QDir(icon_dir).absoluteFilePath('import_fieldbook.png')),
                               tr("Import fieldbook ..."), self.iface.mainWindow())
        self.sc_addp = QAction(QIcon(QDir(icon_dir).absoluteFilePath('addp.png')), tr("Add new point ..."),
                               self.iface.mainWindow())
        self.sc_calc = QAction(QIcon(QDir(icon_dir).absoluteFilePath('single_calc.png')),
                               tr("Single point calculations ..."), self.iface.mainWindow())
        self.sc_trav = QAction(QIcon(QDir(icon_dir).absoluteFilePath('traverse_calc.png')),
                               tr("Traverse calculations ..."), self.iface.mainWindow())
        self.sc_netw = QAction(QIcon(QDir(icon_dir).absoluteFilePath('network_calc.png')), tr("Network adjustment ..."),
                               self.iface.mainWindow())
        self.sc_tran = QAction(QIcon(QDir(icon_dir).absoluteFilePath('coord_calc.png')),
                               tr("Coordinate transformation ..."), self.iface.mainWindow())
        self.sc_pdiv = QAction(QIcon(QDir(icon_dir).absoluteFilePath('poly_div.png')), tr("Polygon division ..."),
                               self.iface.mainWindow())
        self.sc_plot = QAction(QIcon(QDir(icon_dir).absoluteFilePath('plot.png')), tr("Plot by template ..."),
                               self.iface.mainWindow())
        self.sc_batchplot = QAction(QIcon(QDir(icon_dir).absoluteFilePath('batch_plot.png')), tr("Batch plotting ..."),
                                    self.iface.mainWindow())
        self.sc_settings = QAction(tr("Settings ..."), self.iface.mainWindow())
        self.sc_help = QAction(tr("Help"), self.iface.mainWindow())
        self.sc_about = QAction(tr("About"), self.iface.mainWindow())
        self.menu.addActions([self.sc_coord, self.sc_fb, self.sc_load,
                              self.sc_addp, self.sc_calc, self.sc_trav, self.sc_netw,
                              self.sc_tran, self.sc_plot, self.sc_batchplot, self.sc_settings,
                              self.sc_help, self.sc_about])
        self.menu.insertSeparator(self.sc_calc)
        self.menu.insertSeparator(self.sc_plot)
        self.menu.insertSeparator(self.sc_settings)
        self.menu.insertSeparator(self.sc_help)
        menu_bar = self.iface.mainWindow().menuBar()
        actions = menu_bar.actions()
        lastAction = actions[len(actions) - 1]
        menu_bar.insertMenu(lastAction, self.menu)

        self.sc_coord.triggered.connect(self.create_coordlist)
        self.sc_fb.triggered.connect(self.create_fb)
        self.sc_load.triggered.connect(self.load_fieldbook)
        self.sc_addp.triggered.connect(self.addp)
        self.sc_calc.triggered.connect(self.calculations)
        self.sc_trav.triggered.connect(self.traverses)
        self.sc_netw.triggered.connect(self.networks)
        self.sc_tran.triggered.connect(self.transformation)
        self.sc_pdiv.setCheckable(True)
        self.tool_pdiv = LineMapTool(self.iface)
        self.tool_pdiv.setAction(self.sc_pdiv)
        self.sc_pdiv.triggered.connect(self.polygon_division)
        self.sc_plot.triggered.connect(self.plot_by_temp)
        self.sc_batchplot.triggered.connect(self.batch_plotting)
        self.sc_settings.triggered.connect(self.settings)
        self.sc_about.triggered.connect(self.about)
        self.sc_help.triggered.connect(self.help)

        # add icons to toolbar
        self.toolbar = self.iface.addToolBar(u'SurveyingCalculation')
        self.toolbar.setObjectName(u'SurveyingCalculation')
        self.toolbar.addActions([self.sc_load, self.sc_addp, self.sc_calc, self.sc_trav,
                                 self.sc_netw, self.sc_tran, self.sc_pdiv, self.sc_plot, self.sc_batchplot])
        self.toolbar.insertSeparator(self.sc_calc)
        self.toolbar.insertSeparator(self.sc_plot)

    def unload(self):
        """ Removes the plugin menu item and icon from QGIS GUI.
        """
        for action in self.actions:
            self.iface.removePluginMenu(
                tr(u'&SurveyingCalculation'),
                action)
            self.iface.removeToolBarIcon(action)
        del self.menu
        del self.toolbar

    def create_coordlist(self):
        """ Create a new coordinate list from template and add to layer list. Layer/file name changed to start with
        'coord\\_' if neccessary.
        """
        ofname, __ = QFileDialog.getSaveFileName(self.iface.mainWindow(),
                                                 tr('QGIS co-ordinate list'),
                                                 filter=tr('Shape file (*.shp)'))
        if not ofname:
            return
        if QRegExp('coord_').indexIn(QFileInfo(ofname).baseName()):
            ofname = QDir.cleanPath(QFileInfo(ofname).absolutePath() +
                                    QDir().separator() + 'coord_' + QFileInfo(ofname).fileName())
        ofbase = QDir.cleanPath(QFileInfo(ofname).absolutePath() +
                                QDir().separator() + QFileInfo(ofname).baseName())
        tempbase = QDir.cleanPath(self.plugin_dir + QDir().separator() +
                                  'template' + QDir().separator() + 'coord_template')
        for ext in ['.shp', '.shx', '.dbf']:
            QFile(tempbase + ext).copy(ofbase + ext)
        coord = QgsVectorLayer(ofbase + '.shp', QFileInfo(ofbase).baseName(), "ogr")
        if coord.isValid():
            QgsProject.instance().addMapLayer(coord)

    def create_fb(self):
        """ Create a new empty fieldbook from template and add to layer list. Layer/file name changed to start with
        'fb\\_' if neccessary.
        """
        ofname, __ = QFileDialog.getSaveFileName(self.iface.mainWindow(),
                                                 tr('New fieldbook'),
                                                 filter=tr('Fieldbook file (*.dbf)'))
        if not ofname:
            return
        if QRegExp('fb_').indexIn(QFileInfo(ofname).baseName()):
            ofname = QDir.cleanPath(QFileInfo(ofname).absolutePath() +
                                    QDir().separator() + 'fb_' + QFileInfo(ofname).fileName())
        ofbase = QDir.cleanPath(QFileInfo(ofname).absolutePath() +
                                QDir().separator() + QFileInfo(ofname).baseName())
        tempbase = QDir.cleanPath(self.plugin_dir + QDir().separator() +
                                  'template' + QDir().separator() + 'fb_template')
        for ext in ['.dbf']:
            QFile(tempbase + ext).copy(ofbase + ext)
        fb = QgsVectorLayer(ofbase + '.dbf', QFileInfo(ofbase).baseName(), 'ogr')
        if fb.isValid():
            QgsProject.instance().addMapLayer(fb)

    def load_fieldbook(self):
        """ Import an electric fieldbook from file (GSI, JOB/ARE, ...)
        """
        if get_coordlist() is None:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"),
                                tr("No coordinate list is opened, coordinates will be lost from the fieldbook"))
        fname, __ = QFileDialog.getOpenFileName(self.iface.mainWindow(),
                                                tr('Electric fieldbook'), config.homedir,
                                                filter=tr('Nikon RAW (*.raw);;'
                                                          'Leica GSI (*.gsi);;'
                                                          'Leica IDX (*.idx);;'
                                                          'Geodimeter JOB/ARE (*.job *.are);;'
                                                          'Sokkia CRD (*.crd);;'
                                                          'SurvCE RW5 (*.rw5);;'
                                                          'STONEX DAT (*.dat);;'
                                                          'Text dump (*.dmp)'))
        if not fname:
            return

        fb_dbf = None
        ofname = None

        # file selected
        # make a copy of dbf template if not are is loaded
        if QRegExp(r'\.are$', Qt.CaseInsensitive).indexIn(fname) == -1:
            # ask for table name
            ofname, __ = QFileDialog.getSaveFileName(self.iface.mainWindow(),
                                                     tr('QGIS fieldbook'),
                                                     QFileInfo(fname).absolutePath(),
                                                     filter=tr('DBF file (*.dbf)'))
            if not ofname:
                return
            # remember last input dir
            config.homedir = QFileInfo(fname).absolutePath()
            config.store_config()

            # start with 'fb_'?
            if QRegExp('fb_').indexIn(QFileInfo(ofname).baseName()):
                ofname = QDir.cleanPath(QFileInfo(ofname).absolutePath() +
                                        QDir().separator() + 'fb_' + QFileInfo(ofname).fileName())
            # extension is .dbf?
            if QRegExp(r'\.dbf$', Qt.CaseInsensitive).indexIn(ofname) == -1:
                ofname += '.dbf'
            tempname = QDir.cleanPath(self.plugin_dir + QDir().separator() +
                                      'template' + QDir().separator() + 'fb_template.dbf')
            if not QFile(tempname).copy(ofname):
                QMessageBox.warning(self.iface.mainWindow(),
                                    tr('File warning'),
                                    tr('Error copying fieldbook template, target file exists?'),
                                    QMessageBox.Ok)
                return
            fb_dbf = QgsVectorLayer(ofname, QFileInfo(ofname).baseName(), "ogr")
            if not fb_dbf or not fb_dbf.isValid():
                QMessageBox.warning(self.iface.mainWindow(),
                                    tr('File warning'),
                                    tr('Fieldbook loading error'),
                                    QMessageBox.Ok)
                return
            QgsProject.instance().addMapLayer(fb_dbf)

        if QRegExp(r'\.gsi$', Qt.CaseInsensitive).indexIn(fname) > -1:
            fb = LeicaGsi(fname)
        elif QRegExp(r'\.job$', Qt.CaseInsensitive).indexIn(fname) > -1 or \
                QRegExp(r'\.are$', Qt.CaseInsensitive).indexIn(fname) > -1:
            fb = JobAre(fname)
        elif QRegExp(r'\.crd$', Qt.CaseInsensitive).indexIn(fname) > -1:
            fb = Sdr(fname)
        elif QRegExp(r'\.rw5$', Qt.CaseInsensitive).indexIn(fname) > -1:
            fb = SurvCE(fname)
        elif QRegExp(r'\.dat$', Qt.CaseInsensitive).indexIn(fname) > -1:
            fb = Stonex(fname)
        elif QRegExp(r'\.dmp$', Qt.CaseInsensitive).indexIn(fname) > -1:
            fb = Dump(fname)
        elif QRegExp(r'\.idx$', Qt.CaseInsensitive).indexIn(fname) > -1:
            fb = Idex(fname)
        elif QRegExp(r'\.raw$', Qt.CaseInsensitive).indexIn(fname) > -1:
            fb = NikonRaw(fname)
        else:
            QMessageBox.warning(self.iface.mainWindow(),
                                tr('File warning'),
                                tr('Unknown fieldbook type'),
                                QMessageBox.Ok)
            return
        i = 10  # ordinal number for fieldbook records
        # fb_dbf.startEditing()
        fb.open()
        n_fb = 0  # fieldbook records stored
        n_co = 0  # points stored in coordinate list
        while True:
            # get next observation/station data from fieldbook
            r = fb.parse_next()
            if r is None:
                break  # end of file
            if 'station' in r:
                # add row to fieldbook table
                record = QgsFeature()
                # add & initialize attributes
                record.setFields(fb_dbf.fields(), True)
                j = fb_dbf.dataProvider().fieldNameIndex('id')
                if j != -1:
                    record.setAttribute(j, i)
                for key in r:
                    j = fb_dbf.dataProvider().fieldNameIndex(key)
                    if j != -1:
                        record.setAttribute(j, r[key])
                (xxx, yyy) = fb_dbf.dataProvider().addFeatures([record])
                if not xxx:
                    QMessageBox.warning(self.iface.mainWindow(),
                                        tr('File warning'),
                                        tr('Fieldbook record creation error'),
                                        tr('OK'))
                    return
                n_fb += 1
            if 'station_e' in r or 'station_z' in r:
                # store station coordinates too
                dimension = 0
                if 'station_z' in r:
                    dimension += 1
                else:
                    r['station_z'] = None
                if 'station_e' in r and 'station_n' in r:
                    dimension += 2
                else:
                    r['station_e'] = None
                    r['station_n'] = None
                if 'pc' not in r:
                    r['pc'] = None
                if 'pt' not in r:
                    r['pt'] = None
                p = Point(r['point_id'], r['station_e'], r['station_n'], r['station_z'], r['pc'], r['pt'])
                qp = ScPoint(p)
                qp.store_coord(dimension)
                n_co += 1
            if 'e' in r or 'z' in r:
                # store coordinates too
                dimension = 0
                if 'z' in r:
                    dimension += 1
                else:
                    r['z'] = None
                if 'e' in r and 'n' in r:
                    dimension += 2
                else:
                    r['e'] = None
                    r['n'] = None
                if 'pc' not in r:
                    r['pc'] = None
                if 'pt' not in r:
                    r['pt'] = None
                p = Point(r['point_id'], r['e'], r['n'], r['z'], r['pc'], r['pt'])
                qp = ScPoint(p)
                qp.store_coord(dimension)
                n_co += 1
            i += 10
        # fb_dbf.commitChanges()
        if QRegExp(r'\.are$', Qt.CaseInsensitive).indexIn(fname) == -1:
            if n_fb == 0:  # no observations
                QgsProject.instance().removeMapLayer(fb_dbf.id())
                # remove empty file
                QFile(ofname).remove()
                if n_co == 0:  # no coordinates
                    QMessageBox.warning(self.iface.mainWindow(), tr("Warning"),
                                        tr("Neither coordinates nor observations found"))
                else:
                    QMessageBox.warning(self.iface.mainWindow(), tr("Warning"),
                                        tr("No observations found"))
        self.log.write()
        self.log.write_log(tr("Fieldbook loaded: ") + fname)
        self.log.write("    %d observations, %d coordinates" % (n_fb, n_co))

    def addp(self):
        """ Add point(s) to coordinate list entering coordinates
        """
        if get_coordlist() is None:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("A coordinate list must be opened!"))
            return
        # show the dialog
        self.newp_dlg.show()
        self.newp_dlg.activateWindow()
        # Run the dialog event loop
        self.newp_dlg.exec_()

    def calculations(self):
        """ Single point calculations (orientation, intersection,
            resection, freestation)
        """
        # show the dialog
        self.single_dlg.show()
        self.single_dlg.activateWindow()
        # Run the dialog event loop
        self.single_dlg.exec_()

    def traverses(self):
        """ Various traverse claculations
        """
        # show the dialog
        self.traverse_dlg.show()
        self.traverse_dlg.activateWindow()
        # Run the dialog event loop
        self.traverse_dlg.exec_()

    def networks(self):
        """ Various network adjustments (1D/2D/3D)
        """
        # show the dialog
        self.network_dlg.show()
        self.network_dlg.activateWindow()
        # Run the dialog event loop
        self.network_dlg.exec_()

    def transformation(self):
        """ Various coordinate transformations (orthogonal, affine, polynomial)
        """
        # show the dialog
        self.transformation_dlg.show()
        self.transformation_dlg.activateWindow()
        # Run the dialog event loop
        self.transformation_dlg.exec_()

    def polygon_division(self):
        """ accept a line from the user to divide the selected polygon on
            active layer
        """
        al = self.iface.activeLayer()
        if al is None or al.type() != QgsMapLayer.VectorLayer or \
                al.geometryType() != QgsWkbTypes.Polygon:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("Actual layer contains no polygons"))
            return
        if len(al.selectedFeatures()) != 1:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"),
                                tr("Not a single polygon is selected in active layer"))
            return
        self.iface.mapCanvas().setMapTool(self.tool_pdiv)

    def plot_by_temp(self):
        # show the dialog
        # self.plotbytemplate_dlg.show()
        # self.plotbytemplate_dlg.activateWindow()
        # Run the dialog event loop
        # result = self.plotbytemplate_dlg.exec_()
        pass

    def batch_plotting(self):
        """ Batch plots selected geometry items using the selected template and scale.
        """
        # check if there are polygon layers in the project
        polygon_layers = get_vector_layers_by_type(QgsWkbTypes.Polygon)
        if polygon_layers is None:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"),
                                tr("This utility needs at least one polygon type layer!"))
            return

        # show the dialog
        # self.batchplotting_dlg.show()
        # self.batchplotting_dlg.activateWindow()
        # Run the dialog event loop
        # result = self.batchplotting_dlg.exec_()

    def settings(self):
        """ Setting of the plugin.
        """
        settings_dlg = PluginSettingsDialog()
        result = settings_dlg.exec_()
        if result == QDialog.Accepted:
            self.log.set_log_path(config.log_path)

    def about(self):
        """ About box of the plugin
        """
        QMessageBox.information(self.iface.mainWindow(),
                                tr('About'),
                                tr('Surveying Calculation Plugin\n\n (c) DigiKom Ltd 2014- '
                                   'http://digikom.hu, mail (at) digikom.hu\nVersion 0.2'))

    def help(self):
        """ Open user's guide of the plugin in the default web browser.
        """
        webbrowser.open("http://www.digikom.hu/SurveyingCalculation/usersguide.html")
