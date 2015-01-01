# -*- coding: utf-8 -*-
"""
.. module:: surveying_calculation
    :platform: Linux, Windows
    :synopsis: main module

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>

"""
# generic python modules
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant
from PyQt4.QtGui import QAction, QIcon, QMenu, QMessageBox, QFileDialog, QDialog
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
import os.path
from os import unlink
import re
from shutil import copyfile
# debugging
from PyQt4.QtCore import pyqtRemoveInputHook
import pdb

# plugin specific python modules
import config
from base_classes import tr
from new_point_dialog import NewPointDialog
from single_dialog import SingleDialog
from traverse_dialog import TraverseDialog
from network_dialog import NetworkDialog
from transformation_dialog import TransformationDialog
from batch_plotting_dialog import BatchPlottingDialog
from totalstations import *
from surveying_util import *
from calculation import *
from resultlog import *
from line_tool import LineMapTool

import sys
#sys.path.append(r'C:\Program Files\eclipse-standard-luna-R-win32-x86_64\eclipse\plugins\org.python.pydev_3.8.0.201409251235\pysrc')
#import pydevd

class SurveyingCalculation:
    """SurveyingCalculation QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: an interface instance that will be passed to this class which provides the hook by which you can manipulate the QGIS application at run time (QgsInterface)
        """
        #pydevd.settrace()
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'surveying_calculation_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # init result log
        if hasattr(config, 'log_path') and len(config.log_path) > 0:
            log_path = config.log_path
        else:
            log_path = os.path.join(self.plugin_dir,'log','log.txt')
        self.log = ResultLog(log_path)

        self.newp_dlg = NewPointDialog()
        self.single_dlg = SingleDialog(self.log)
        self.traverse_dlg = TraverseDialog(self.log)
        self.network_dlg = NetworkDialog(self.log)
        self.transformation_dlg = TransformationDialog(self.log)
        self.plotbytemplate_dlg = BatchPlottingDialog(self.iface, False)
        self.batchplotting_dlg = BatchPlottingDialog(self.iface, True)
        
        # Declare instance attributes

    # noinspection PyMethodMayBeStatic
    #def tr(self, message):
    #    """Get the translation for a string using Qt translation API. We implement this ourselves since we do not inherit QObject.

    #    :param message: string for translation (str, QString)
    #    :returns: translated version of message (QString)
    #    """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        #return QCoreApplication.translate('SurveyingCalculation', message)
    #    return tr(message)

    def add_action(self, icon_path, text, callback, enabled_flag=True,
        add_to_menu=True, add_to_toolbar=True, status_tip=None,
        whats_this=None, parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.

        :param icon_path: path to the icon for this action. Can be a resource path (e.g. ':/plugins/foo/bar.png') or a normal file system path (str)
        :param text: text that should be shown in menu items for this action (str)
        :param callback: function to be called when the action is triggered (function)
        :param enabled_flag: a flag indicating if the action should be enabled by default (bool). Defaults to True.
        :param add_to_menu: flag indicating whether the action should also be added to the menu (bool). Defaults to True.
        :param add_to_toolbar: flag indicating whether the action should also be added to the toolbar (bool). Defaults to True.
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

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/SurveyingCalculation/icon.png'
        # build menu
        self.actions = []
        self.menu = QMenu()
        self.menu.setTitle(tr(u'&SurveyingCalculation'))
        self.sc_coord = QAction(QIcon(os.path.join(self.plugin_dir,'icons','new_coord.png')), tr("New coordinate list ..."), self.iface.mainWindow())
        self.sc_fb = QAction(QIcon(os.path.join(self.plugin_dir,'icons','new_fb.png')),tr("New fieldbook ..."), self.iface.mainWindow())
        self.sc_load = QAction(QIcon(os.path.join(self.plugin_dir,'icons','import_fieldbook.png')), tr("Import fieldbook ..."), self.iface.mainWindow())
        self.sc_addp = QAction(QIcon(os.path.join(self.plugin_dir,'icons','addp.png')), tr("Add new point ..."), self.iface.mainWindow())
        self.sc_calc = QAction(QIcon(os.path.join(self.plugin_dir,'icons','single_calc.png')), tr("Single point calculations ..."), self.iface.mainWindow())
        self.sc_trav = QAction(QIcon(os.path.join(self.plugin_dir,'icons','traverse_calc.png')), tr("Traverse calculations ..."), self.iface.mainWindow())
        self.sc_netw = QAction(QIcon(os.path.join(self.plugin_dir,'icons','network_calc.png')), tr("Network adjustment ..."), self.iface.mainWindow())
        self.sc_tran = QAction(QIcon(os.path.join(self.plugin_dir,'icons','coord_calc.png')), tr("Coordinate transformation ..."), self.iface.mainWindow())
        self.sc_pdiv = QAction(QIcon(os.path.join(self.plugin_dir,'icons','poly_div.png')), tr("Polygon division ..."), self.iface.mainWindow())
        self.sc_plot = QAction(QIcon(os.path.join(self.plugin_dir,'icons','plot.png')), tr("Plot by template ..."), self.iface.mainWindow())
        self.sc_batchplot = QAction(QIcon(os.path.join(self.plugin_dir,'icons','batch_plot.png')), tr("Batch plotting ..."), self.iface.mainWindow())
        self.sc_help = QAction(tr("Help"), self.iface.mainWindow())
        self.sc_about = QAction(tr("About"), self.iface.mainWindow())
        self.menu.addActions([self.sc_coord, self.sc_fb, self.sc_load,
            self.sc_addp, self.sc_calc, self.sc_trav, self.sc_netw,
            self.sc_tran, self.sc_plot, self.sc_batchplot, self.sc_help,
            self.sc_about])
        self.menu.insertSeparator(self.sc_calc)
        self.menu.insertSeparator(self.sc_plot)
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
        """ Create a new coordinate list from template and add to layer list. Layer/file name changed to start with 'coord\_' if neccessary.
        """
        ofname = QFileDialog.getSaveFileName(self.iface.mainWindow(),
            tr('QGIS co-ordinate list'),
            filter = tr('Shape file (*.shp)'))
        if not ofname:
            return
        if not re.match('coord_', os.path.basename(ofname)):
            ofname = os.path.join(os.path.dirname(ofname),
                'coord_' + os.path.basename(ofname))
        ofbase = os.path.splitext(ofname)[0]
        tempbase = os.path.join(self.plugin_dir, 'template', 'coord_template')
        for ext in ['.shp', '.shx', '.dbf']:
            copyfile(tempbase+ext, ofbase+ext)
        coord = QgsVectorLayer(ofbase+'.shp', os.path.splitext(os.path.basename(ofname))[0], "ogr")
        if coord.isValid():
            QgsMapLayerRegistry.instance().addMapLayer(coord)

    def create_fb(self):
        """ Create a new empty fieldbook from template and add to layer list. Layer/file name changed to start with 'fb\_' if neccessary.
        """
        ofname = QFileDialog.getSaveFileName(self.iface.mainWindow(),
            tr('New fieldbook'),
            filter = tr('Fieldbook file (*.dbf)'))
        if not ofname:
            return
        if not re.match('fb_', os.path.basename(ofname)):
            ofname = os.path.join(os.path.dirname(ofname),
                'fb_' + os.path.basename(ofname))
        ofbase = os.path.splitext(ofname)[0]
        tempbase = os.path.join(self.plugin_dir, 'template', 'fb_template')
        for ext in ['.dbf']:
            copyfile(tempbase+ext, ofbase+ext)
        fb = QgsVectorLayer(ofbase+ext, os.path.splitext(os.path.basename(ofname))[0], "ogr")
        if fb.isValid():
            QgsMapLayerRegistry.instance().addMapLayer(fb)

    def load_fieldbook(self):
        """ Import an electric fieldbook from file (GSI, JOB/ARE, ...)
        """
        if get_coordlist() is None:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("No coordinate list is opened, coordinates will be lost from the fieldbook"))
        fname = QFileDialog.getOpenFileName(self.iface.mainWindow(), \
            tr('Electric fieldbook'), config.homedir, \
            filter = tr('Leica GSI (*.gsi);;Geodimeter JOB/ARE (*.job *.are);;Sokkia CRD (*.crd);;SurvCE RW5 (*.rw5);;STONEX DAT (*.dat)'))
        if fname:
            # file selected
            # make a copy of dbf template if not are is loaded
            if not re.search('\.are$', fname, re.IGNORECASE):
                # ask for table name
                ofname = QFileDialog.getSaveFileName(self.iface.mainWindow(),
                    tr('QGIS fieldbook'),
                    os.path.split(fname)[0],
                    filter = tr('DBF file (*.dbf)'))
                if not ofname:
                    return
                # remember last input dir
                config.homedir = os.path.dirname(fname)
                if not re.match('fb_', os.path.basename(ofname)):
                    ofname = os.path.join(os.path.dirname(ofname),
                        'fb_' + os.path.basename(ofname) + '.dbf')
                copyfile(os.path.join(self.plugin_dir, 'template', 'fb_template.dbf'), ofname)
                fb_dbf = QgsVectorLayer(ofname, os.path.splitext(os.path.basename(ofname))[0], "ogr")
                QgsMapLayerRegistry.instance().addMapLayer(fb_dbf)
            if re.search('\.gsi$', fname, re.IGNORECASE):
                fb = LeicaGsi(fname)
            elif re.search('\.job$', fname, re.IGNORECASE) or \
                re.search('\.are$', fname, re.IGNORECASE):
                fb = JobAre(fname)
            elif re.search('\.crd$', fname, re.IGNORECASE):
                fb = Sdr(fname)
            elif re.search('\.rw5$', fname, re.IGNORECASE):
                fb = SurvCE(fname)
            elif re.search('\.dat$', fname, re.IGNORECASE):
                fb = Stonex(fname)
            else:
                QMessageBox.warning(self.iface.mainWindow(),
                    tr('File warning'),
                    tr('Unknown fieldbook type'),
                    tr('OK'))
                return
            i = 10    # ordinal number for fieldbook records
            #fb_dbf.startEditing()
            fb.open()
            n_fb = 0    # fieldbook records stored
            n_co = 0    # points stored in coordinate list
            while True:
                # get next observation/station data from fieldbook
                r = fb.parse_next()
                if r is None:
                    break    # end of file
                if 'station' in r:
                    # add row to fieldbook table
                    record = QgsFeature()
                    # add & initialize attributes
                    record.setFields(fb_dbf.pendingFields(), True)
                    j = fb_dbf.dataProvider().fieldNameIndex('id')
                    if j != -1:
                        record.setAttribute(j, i)
                    for key in r:
                        j = fb_dbf.dataProvider().fieldNameIndex(key)
                        if j != -1:
                            record.setAttribute(j, r[key])
                    fb_dbf.dataProvider().addFeatures([record])
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
                    if not 'pc' in r:
                        r['pc'] = None
                    p = Point(r['point_id'], r['station_e'], r['station_n'], r['station_z'], r['pc'])
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
                    if not 'pc' in r:
                        r['pc'] = None
                    p = Point(r['point_id'], r['e'], r['n'], r['z'], r['pc'])
                    qp = ScPoint(p)
                    qp.store_coord(dimension)
                    n_co += 1
                i += 10
            #fb_dbf.commitChanges()
            if not re.search('\.are$', fname, re.IGNORECASE):
                if n_fb == 0:        # no observations
                    QgsMapLayerRegistry.instance().removeMapLayer(fb_dbf.id())
                    # remove empty file
                    unlink(ofname)
                    if n_co == 0:    # no coordinates
                        QMessageBox.warning(self.iface.mainWindow(), tr("Warning"),\
                            tr("Neither coordinates nor observations found"))
                    else:
                        QMessageBox.warning(self.iface.mainWindow(), tr("Warning"),\
                            tr("No observations found"))
            self.log.write()
            self.log.write_log(tr("Fieldbook loaded: ") + fname)
            self.log.write("    %d observations, %d coordinates" % (n_fb, n_co))
        return
    
    def addp(self):
        """ Add point(s) to coordinate list entering coordinates
        """
        if get_coordlist() is None:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("A coordinate list must be opened!"))
            return
        # show the dialog
        self.newp_dlg.show()
        # Run the dialog event loop
        result = self.newp_dlg.exec_()

    def calculations(self):
        """ Single point calculations (orientation, intersection,
            resection, freestation)
        """
        # show the dialog
        self.single_dlg.show()
        # Run the dialog event loop
        result = self.single_dlg.exec_()

    def traverses(self):
        """ Various traverse claculations
        """
        # show the dialog
        self.traverse_dlg.show()
        # Run the dialog event loop
        result = self.traverse_dlg.exec_()

    def networks(self):
        """ Various network adjustments (1D/2D/3D)
        """
        # show the dialog
        self.network_dlg.show()
        # Run the dialog event loop
        result = self.network_dlg.exec_()

    def transformation(self):
        """ Various coordinate transformations (orthogonal, affine, polynomial)
        """
        # show the dialog
        self.transformation_dlg.show()
        # Run the dialog event loop
        result = self.transformation_dlg.exec_()
        
    def polygon_division(self):
        """ accept a line from the user to divide the selected polygon on 
            active layer
        """
        al = self.iface.activeLayer()
        if al is None or al.type() != QgsMapLayer.VectorLayer or \
            al.geometryType() != QGis.Polygon:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("Actual layer contains no polygons"))
            return
        if len(al.selectedFeatures()) != 1:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("Not a single polygon is selected in active layer"))
            return
        self.iface.mapCanvas().setMapTool(self.tool_pdiv)

    def plot_by_temp(self):
        # show the dialog
        self.plotbytemplate_dlg.show()
        # Run the dialog event loop
        result = self.plotbytemplate_dlg.exec_()

    def batch_plotting(self):
        """ Batch plots selected geometry items using the selected template and scale.
        """
        #check if there are polygon layers in the project
        polygon_layers = get_vector_layers_by_type(QGis.Polygon)
        if polygon_layers is None:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"),
                tr("This utility needs at least one polygon type layer!"))
            return

        # show the dialog
        self.batchplotting_dlg.show()
        # Run the dialog event loop
        result = self.batchplotting_dlg.exec_()
        
    def about(self):
        """ About box of the plugin
        """
        QMessageBox.information(self.iface.mainWindow(),
            tr('About'),    
            tr('Surveying Calculation Plugin\n\n (c) DigiKom Ltd 2014 http://digikom.hu mail (at) digikom.hu\nVersion 0.1a'))

    def help(self):
        # TODO
        pass
