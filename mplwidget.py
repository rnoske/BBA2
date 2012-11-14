# -*- coding: utf-8 -*-

# for command-line arguments
import sys
# Python Qt4 bindings for GUI objects
from PyQt4 import QtGui
# Numpy functions for image creation
import numpy as np
# Matplotlib Figure object
from matplotlib.figure import Figure
import matplotlib as mpl
# import the Qt4Agg FigureCanvas object, that binds Figure to
# Qt4Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt4agg \
  import FigureCanvasQTAgg as FigureCanvas
# import the NavigationToolbar Qt4Agg widget
from matplotlib.backends.backend_qt4agg \
  import NavigationToolbar2QTAgg as NavigationToolbar
    
    

class Qt4MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self, parent):
        # plot definition
        self.fig = Figure()
        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.x = []
        self.y = []
        #self.axes.set_autoscale_on(True)
        self.axes.plot(self.x, self.y) 
        #self.fig.canvas.draw()
        # set the parent widget
        self.setParent(parent)
        # we define the widget as expandable
        FigureCanvas.setSizePolicy(self, 
                                   QtGui.QSizePolicy.Expanding, 
                                   QtGui.QSizePolicy.Expanding) 
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)
        
    def updatePlot(self, x, y):
        """ Updates plot window
        
        x (arr): x values
        y (arr): y values
        
        """
        self.axes.clear()
        self.x = x
        self.y = y
        #self.fig.canvas.draw()
        self.axes.plot(self.x, self.y)
        mpl.axes.Axes.relim(self.axes)
        self.fig.canvas.draw()
        
    def updatePlot_2y(self, x, y, y2):
        """ Updates plot window
        
        x (arr): x values
        y (arr): y values
        y2 (arr): y2 values
        
        """
        self.axes.clear()
        self.x = x
        self.y = y
        self.y2 = y2
        #self.fig.canvas.draw()
        self.axes.plot(self.x, self.y, self.x, self.y2)
        mpl.axes.Axes.relim(self.axes)
        self.fig.canvas.draw()
        
    
        
    def update_plot_verrbar(self, x, y, errbar):
        """ Update plot with errorbars
        
        x (arr): x values
        y (arr): y values
        errbar (arr): errors of y values
        
        """
        self.axes.clear()
        #self.x = x
        #self.y = y
        #self.fig.canvas.draw()
        self.axes.errorbar(x, y, yerr = errbar)
        mpl.axes.Axes.relim(self.axes)
        self.fig.canvas.draw()
        
class MplWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        # instantiate a widget, it will be the main one
        self.main_widget = QtGui.QWidget(self)
        # create a vertical box layout widget 
        vbl = QtGui.QVBoxLayout(self.main_widget)
        # instantiate our Matplotlib canvas widget
        self.qmc = Qt4MplCanvas(self.main_widget)
        # instantiate the navigation toolbar
        ntb = NavigationToolbar(self.qmc, self.main_widget)
        # pack these widget into the vertical box
        vbl.addWidget(self.qmc) 
        vbl.addWidget(ntb) 
        # set the focus on the main widget
        self.main_widget.setFocus() 
        # set the central widget of MainWindow to main_widget 
        #self.setCentralWidget(self.main_widget) 
        