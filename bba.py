# -*- coding: utf-8 -*-

"""
Guihandler!
"""

#standard library imports
import sys
import logging

#related third party imports
from PyQt4 import QtGui, QtCore

#local application/library specific imports
import BBAgui #from BBAgui import Ui_BBA
import Settingsui #from Settingsui import Ui_Settings
import Plotterui

class Bba(QtGui.QMainWindow):
    """ Gui handler class
    
    """
    def __init__(self, parent=None):
        """ Initialisation
        
        """
        QtGui.QWidget.__init__(self, parent)
        self.ui = BBAgui.Ui_BBA()
        self.ui.setupUi(self)
        self.show()
        
        #self.bba = BBA()
    
    #open image call answear
    def openImages(self):
        """ Responds to dialog to open images
        
        """
        _msg = 'Select one or more images to open'
        _prepath = 'D:/Raimund Buero/Python/testbilder'
        _Imagetypes = 'Images (*.bmp *.png *.jpg *.fit *.fits)'
        filepaths = QtGui.QFileDialog.getOpenFileNames(self, 
                                                      _msg,
                                                      _prepath, 
                                                      _Imagetypes)
        for filepath in filepaths:
            self.bba.add_image_bd(str(filepath))
        _nL = self.bba.get_imageName_list()
        for name in _nL:
            _fp = QtGui.QListWidgetItem(name, self.ui.ImageList)
            self.ui.ImageList.addItem(_fp)
            
        #Set Image settings
        try:
            self.setImageSettings()
        except:
            logging.error('Fehler beim schreiben der Settings beim \
            oeffnen der Datei')
        
    #Settings function
    def openSettings(self, parent = None):
        """ Responds to open Settings call from Settings.ui
        
        """
        QtGui.QWidget.__init__(self, parent)
        self.sui = Settingsui.Ui_Settings()
        self.sui.setupUi(self)
        self.show()
        
        #Initialize values by reading Settings.ini
        self.loadSettings()

    def loadSettings(self):
        """ Respond to load settings call
        
        Reads values out of Settings.ini and sends them to gui
        
        """
        _setDict = self.bba.get_settings() #gets dict
        #Write to GUI
        try:
            #Nullpunkt
            _val = int(_setDict['nullpunkt'])
            self.sui.Nullhoehe.setValue(_val)
            #Flammenmitte
            _val = int(_setDict['flammenmitte'])
            self.sui.Flammenmitte.setValue(_val)
            #Grad zwischen den Bildern
            _val = int(_setDict['gradprobild'])
            self.sui.GradZwischenBildern.setValue(_val)
            #Aufloesung
            _val = float(_setDict['aufloesung'])
            self.sui.Aufloesung.setValue(_val)
            #Workspace
            _val = _setDict['workspace']
            self.sui.WorkspaceShow_label.setText(_val)
        except:
            logging.ERROR('Settings konnten nicht gesetzt werden')
    
    def saveSettings(self):
        """ Save current Settings in Settings.ini
        
        """
        _setDict = {}
        try:
            _setDict['nullpunkt'] = str(self.sui.Nullhoehe.value())
            _setDict['flammenmitte'] = str(self.sui.Flammenmitte.value())
            _setDict['gradprobild'] = str(self.sui.GradZwischenBildern.value())
            _setDict['aufloesung'] = str(self.sui.Aufloesung.value())
            _tmp = self.sui.WorkspaceShow_label.text()
            _tmp = str(_tmp)
            _setDict['workspace'] = _tmp
        except:
            logging.error('Settings konnten nicht von ui gelesen werden')
        
        try:
            self.bba.set_settings(_setDict)
        except:
            logging.error('Settings konnten nicht geschrieben werden')
    
    def setImageSettings(self):
        """ Send Settings to each Bild instance
        
        """
        self.bba.setImageSettings()
        
    def chooseWorkspace(self):
        """ File Dialog to choose current workspace
        
        """
        #_file = QtGui.QFileDialog.getOpenFileName(self, _msg, _prepath, _type)
        _dir = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
        self.sui.WorkspaceShow_label.setText(_dir)
            
    #Plotter functions
    def openPlotter(self):
        """ Responds to open Plotter call from Plotter.ui
        
        """
        QtGui.QWidget.__init__(self, parent = None)
        self.pui = Plotterui.Ui_Plotterui()
        self.pui.setupUi(self)
        self.show()
        
        
        


if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   myapp = Bba()
   sys.exit(app.exec_())