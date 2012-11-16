# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BBAgui.ui'
#
# Created: Fri Nov 16 13:59:27 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BBA(object):
    def setupUi(self, BBA):
        BBA.setObjectName(_fromUtf8("BBA"))
        BBA.resize(545, 447)
        self.centralwidget = QtGui.QWidget(BBA)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(1, 1, 281, 411))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ImageList = QtGui.QListWidget(self.layoutWidget)
        self.ImageList.setObjectName(_fromUtf8("ImageList"))
        self.verticalLayout.addWidget(self.ImageList)
        self.OpenImages = QtGui.QPushButton(self.layoutWidget)
        self.OpenImages.setObjectName(_fromUtf8("OpenImages"))
        self.verticalLayout.addWidget(self.OpenImages)
        self.saveResults = QtGui.QPushButton(self.centralwidget)
        self.saveResults.setGeometry(QtCore.QRect(310, 150, 121, 23))
        self.saveResults.setObjectName(_fromUtf8("saveResults"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(310, 11, 122, 136))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.cB_totalIntensity = QtGui.QCheckBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cB_totalIntensity.sizePolicy().hasHeightForWidth())
        self.cB_totalIntensity.setSizePolicy(sizePolicy)
        self.cB_totalIntensity.setObjectName(_fromUtf8("cB_totalIntensity"))
        self.verticalLayout_2.addWidget(self.cB_totalIntensity)
        self.cB_flameHeight = QtGui.QCheckBox(self.widget)
        self.cB_flameHeight.setObjectName(_fromUtf8("cB_flameHeight"))
        self.verticalLayout_2.addWidget(self.cB_flameHeight)
        self.cB_flameArea = QtGui.QCheckBox(self.widget)
        self.cB_flameArea.setObjectName(_fromUtf8("cB_flameArea"))
        self.verticalLayout_2.addWidget(self.cB_flameArea)
        self.cB_flameAreaCounting = QtGui.QCheckBox(self.widget)
        self.cB_flameAreaCounting.setObjectName(_fromUtf8("cB_flameAreaCounting"))
        self.verticalLayout_2.addWidget(self.cB_flameAreaCounting)
        self.pB_Calculate = QtGui.QPushButton(self.widget)
        self.pB_Calculate.setObjectName(_fromUtf8("pB_Calculate"))
        self.verticalLayout_2.addWidget(self.pB_Calculate)
        BBA.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(BBA)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 545, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMein_test = QtGui.QMenu(self.menubar)
        self.menuMein_test.setObjectName(_fromUtf8("menuMein_test"))
        BBA.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(BBA)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        BBA.setStatusBar(self.statusbar)
        self.actionOpen_Images = QtGui.QAction(BBA)
        self.actionOpen_Images.setObjectName(_fromUtf8("actionOpen_Images"))
        self.actionOpen_Image_directory = QtGui.QAction(BBA)
        self.actionOpen_Image_directory.setObjectName(_fromUtf8("actionOpen_Image_directory"))
        self.actionClose = QtGui.QAction(BBA)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionOpen_Settings = QtGui.QAction(BBA)
        self.actionOpen_Settings.setObjectName(_fromUtf8("actionOpen_Settings"))
        self.actionOpen_Plotter = QtGui.QAction(BBA)
        self.actionOpen_Plotter.setObjectName(_fromUtf8("actionOpen_Plotter"))
        self.menuMein_test.addAction(self.actionOpen_Images)
        self.menuMein_test.addAction(self.actionOpen_Image_directory)
        self.menuMein_test.addAction(self.actionClose)
        self.menuMein_test.addAction(self.actionOpen_Settings)
        self.menuMein_test.addAction(self.actionOpen_Plotter)
        self.menubar.addAction(self.menuMein_test.menuAction())

        self.retranslateUi(BBA)
        QtCore.QObject.connect(self.actionClose, QtCore.SIGNAL(_fromUtf8("triggered()")), BBA.close)
        QtCore.QObject.connect(self.OpenImages, QtCore.SIGNAL(_fromUtf8("clicked()")), BBA.openImages)
        QtCore.QObject.connect(self.actionOpen_Settings, QtCore.SIGNAL(_fromUtf8("triggered()")), BBA.openSettings)
        QtCore.QObject.connect(self.actionOpen_Plotter, QtCore.SIGNAL(_fromUtf8("triggered()")), BBA.openPlotter)
        QtCore.QObject.connect(self.pB_Calculate, QtCore.SIGNAL(_fromUtf8("clicked()")), BBA.calculateStuff)
        QtCore.QObject.connect(self.saveResults, QtCore.SIGNAL(_fromUtf8("clicked()")), BBA.saveResults)
        QtCore.QMetaObject.connectSlotsByName(BBA)

    def retranslateUi(self, BBA):
        BBA.setWindowTitle(QtGui.QApplication.translate("BBA", "BBA", None, QtGui.QApplication.UnicodeUTF8))
        self.OpenImages.setText(QtGui.QApplication.translate("BBA", "Open Images", None, QtGui.QApplication.UnicodeUTF8))
        self.saveResults.setText(QtGui.QApplication.translate("BBA", "Save Results", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("BBA", "Calculate:", None, QtGui.QApplication.UnicodeUTF8))
        self.cB_totalIntensity.setText(QtGui.QApplication.translate("BBA", "total Intensity", None, QtGui.QApplication.UnicodeUTF8))
        self.cB_flameHeight.setText(QtGui.QApplication.translate("BBA", "Flame height", None, QtGui.QApplication.UnicodeUTF8))
        self.cB_flameArea.setText(QtGui.QApplication.translate("BBA", "Flame area", None, QtGui.QApplication.UnicodeUTF8))
        self.cB_flameAreaCounting.setText(QtGui.QApplication.translate("BBA", "Flame area counting", None, QtGui.QApplication.UnicodeUTF8))
        self.pB_Calculate.setText(QtGui.QApplication.translate("BBA", "Calculate!", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMein_test.setTitle(QtGui.QApplication.translate("BBA", "Menu", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Images.setText(QtGui.QApplication.translate("BBA", "Open Images", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Image_directory.setText(QtGui.QApplication.translate("BBA", "Open Image directory", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("BBA", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Settings.setText(QtGui.QApplication.translate("BBA", "Open Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Plotter.setText(QtGui.QApplication.translate("BBA", "Open Plotter", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    BBA = QtGui.QMainWindow()
    ui = Ui_BBA()
    ui.setupUi(BBA)
    BBA.show()
    sys.exit(app.exec_())

