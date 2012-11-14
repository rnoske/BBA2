# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Plotterui.ui'
#
# Created: Tue Nov 13 15:22:19 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Plotterui(object):
    def setupUi(self, Plotterui):
        Plotterui.setObjectName(_fromUtf8("Plotterui"))
        Plotterui.setEnabled(True)
        Plotterui.resize(687, 624)
        self.MPLArea = MplWidget(Plotterui)
        self.MPLArea.setGeometry(QtCore.QRect(20, 40, 651, 561))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MPLArea.sizePolicy().hasHeightForWidth())
        self.MPLArea.setSizePolicy(sizePolicy)
        self.MPLArea.setFocusPolicy(QtCore.Qt.NoFocus)
        self.MPLArea.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.MPLArea.setObjectName(_fromUtf8("MPLArea"))
        self.Plot_comboBox = QtGui.QComboBox(Plotterui)
        self.Plot_comboBox.setGeometry(QtCore.QRect(20, 10, 141, 22))
        self.Plot_comboBox.setMaxVisibleItems(100)
        self.Plot_comboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.Plot_comboBox.setObjectName(_fromUtf8("Plot_comboBox"))

        self.retranslateUi(Plotterui)
        QtCore.QObject.connect(self.Plot_comboBox, QtCore.SIGNAL(_fromUtf8("activated(int)")), Plotterui.myPlot)
        QtCore.QMetaObject.connectSlotsByName(Plotterui)

    def retranslateUi(self, Plotterui):
        Plotterui.setWindowTitle(QtGui.QApplication.translate("Plotterui", "Plotter", None, QtGui.QApplication.UnicodeUTF8))

from mplwidget import MplWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Plotterui = QtGui.QWidget()
    ui = Ui_Plotterui()
    ui.setupUi(Plotterui)
    Plotterui.show()
    sys.exit(app.exec_())

