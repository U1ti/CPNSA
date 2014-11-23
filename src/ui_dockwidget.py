# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dockwdiget.ui'
#
# Created: Fri May 03 15:55:33 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(400, 300)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scanButton = QtGui.QPushButton(self.dockWidgetContents)
        self.scanButton.setObjectName(_fromUtf8("scanButton"))
        self.verticalLayout.addWidget(self.scanButton)
        self.sniffButton = QtGui.QPushButton(self.dockWidgetContents)
        self.sniffButton.setObjectName(_fromUtf8("sniffButton"))
        self.verticalLayout.addWidget(self.sniffButton)
        self.testMap = QtGui.QPushButton(self.dockWidgetContents)
        self.testMap.setObjectName(_fromUtf8("testMap"))
        self.verticalLayout.addWidget(self.testMap)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "DockWidget", None))
        self.scanButton.setText(_translate("DockWidget", "Scan", None))
        self.sniffButton.setText(_translate("DockWidget", "Sniff", None))
        self.testMap.setText(_translate("DockWidget", "PushButton", None))

