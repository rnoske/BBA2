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

import ph

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
        
        self.ph = ph.Ph()
    
    #open image call answear
    def openImages(self):
        """ Responds to dialog to open images
        
        """
        #get settings
        _setDict = self.ph.get_settings(section='FlameParameters') #gets dict
        
        _msg = 'Select one or more images to open'
        try:
            _prepath = _setDict['openimagepath']
        except (KeyError):
            _prepath = 'D:/Raimund Buero/Python/testbilder'
            
        _Imagetypes = 'Images (*.bmp *.png *.jpg *.fit *.fits)'
        filepaths = QtGui.QFileDialog.getOpenFileNames(self, 
                                                      _msg,
                                                      _prepath, 
                                                      _Imagetypes)
        #delete old image list
        self.ph.del_image_dict()
        #add new images to dict
        for filepath in filepaths:
            self.ph.add_image_bd(str(filepath))
        _nL = self.ph.get_imageName_list()
        #Gui handling
        self.ui.ImageList.clear()
        for name in _nL:
            _fp = QtGui.QListWidgetItem(name, self.ui.ImageList)
            self.ui.ImageList.addItem(_fp)
            
        #Set Image settings
        self.setImageSettings()
        
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
        _setDict = self.ph.get_settings(section='FlameParameters')
        self.ph.setImageSettings(_setDict)
        
    def chooseWorkspace(self):
        """ File Dialog to choose current workspace
        
        """
        #_file = QtGui.QFileDialog.getOpenFileName(self, _msg, _prepath, _type)
        _dir = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
        self.sui.WorkspaceShow_label.setText(_dir)
        
    #Calculate stuff
    def calculateStuff(self):
        """ Answears calculate stuff call
        
        """
        if self.ui.cB_convertjpg.checkState() == 2:
            self.ph.convert_jpg()
        if self.ui.cB_totalIntensity.checkState() == 2:
            self.ph.calc_totalInt()
        if self.ui.cB_flameHeight.checkState() ==2:
            self.ph.calc_flameHeight()
        if self.ui.cB_flameArea.checkState() == 2:
            self.ph.calc_flameArea()
        if self.ui.cB_flameAreaCounting.checkState() == 2:
            self.ph.calc_flameAreaCounting()
            
    def saveResults(self):
        """ Answears save results call
        
        """
        self.ph.save_ResultData()
            
    #Plotter functions
    def openPlotter(self):
        """ Responds to open Plotter call from Plotter.ui
        
        """
        QtGui.QWidget.__init__(self, parent = None)
        self.pui = Plotterui.Ui_Plotterui()
        self.pui.setupUi(self)
        self.show()
        
        #call myPlot to display something
        self.myPlot()
        
    def myPlot(self):
        """ Responds to event from Plot_button from Plotter.ui
        
        """
        #add possible data to plot
        _pD = self.ph.data
        #shortcut to comboBox
        _cB = self.pui.Plot_comboBox
        
        _seen = []
        for i in range(_cB.count()):
            _cB_c = _cB.itemData(i, 0).toString()
            _cB_c = str(_cB_c) #convert pyqt string to normal string
            if _cB_c not in _seen:
                _seen.append(_cB_c)

        for key in _pD.keys():
            if key not in _seen:
                _val = QtCore.QVariant(key) #convert to QVariant
                #_cB.setItemData(i, _val, 0)
                _cB.addItem(key, _val)
        
        #current item index
        _cB_index = _cB.currentIndex() 
        #get Variant Object as pyqt string object
        _cB_c = _cB.itemData(_cB_index, 0).toString()
        _cB_c = str(_cB_c) #convert pyqt string to normal string
        
        if len(_pD) != 0:
            data = _pD[_cB_c]
            if data.shape[1] == 2:
                _x = data[:, 0]
                _y = data[:, 1]
                self.pui.MPLArea.qmc.updatePlot(_x,_y)
            elif data.shape[1] == 3:
                _x = data[:, 0]
                _y = data[:, 1]
                _y2 = data[:, 2]
                self.pui.MPLArea.qmc.updatePlot_2y(_x,_y, _y2)
        
        
        


if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   myapp = Bba()
   sys.exit(app.exec_())