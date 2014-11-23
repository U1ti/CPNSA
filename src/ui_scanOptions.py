# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scanOptions.ui'
#
# Created: Sun Jun 09 15:04:36 2013
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

class Ui_scanOptions(object):
    def setupUi(self, scanOptions):
        scanOptions.setObjectName(_fromUtf8("scanOptions"))
        scanOptions.resize(510, 297)
        self.gridLayout_3 = QtGui.QGridLayout(scanOptions)
        self.gridLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(scanOptions)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_2 = QtGui.QLabel(scanOptions)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.label = QtGui.QLabel(scanOptions)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.comboBox = QtGui.QComboBox(scanOptions)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.verticalLayout.addWidget(self.comboBox)
        self.commandEdit = QtGui.QLineEdit(scanOptions)
        self.commandEdit.setObjectName(_fromUtf8("commandEdit"))
        self.verticalLayout.addWidget(self.commandEdit)
        self.targetEdit = QtGui.QLineEdit(scanOptions)
        self.targetEdit.setObjectName(_fromUtf8("targetEdit"))
        self.verticalLayout.addWidget(self.targetEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(349, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 1, 0, 1, 2)
        self.moreButton = QtGui.QPushButton(scanOptions)
        self.moreButton.setCheckable(True)
        self.moreButton.setObjectName(_fromUtf8("moreButton"))
        self.gridLayout_3.addWidget(self.moreButton, 1, 2, 1, 1)
        self.moreFrame = QtGui.QFrame(scanOptions)
        self.moreFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.moreFrame.setFrameShadow(QtGui.QFrame.Sunken)
        self.moreFrame.setObjectName(_fromUtf8("moreFrame"))
        self.gridLayout = QtGui.QGridLayout(self.moreFrame)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tableWidget = QtGui.QTableWidget(self.moreFrame)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.moreFrame, 2, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(scanOptions)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 4, 1, 1, 2)
        self.label_3.setBuddy(self.comboBox)
        self.label_2.setBuddy(self.commandEdit)
        self.label.setBuddy(self.targetEdit)

        self.retranslateUi(scanOptions)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), scanOptions.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), scanOptions.reject)
        QtCore.QObject.connect(self.moreButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.moreFrame.setVisible)
        QtCore.QMetaObject.connectSlotsByName(scanOptions)
        scanOptions.setTabOrder(self.comboBox, self.commandEdit)
        scanOptions.setTabOrder(self.commandEdit, self.targetEdit)
        scanOptions.setTabOrder(self.targetEdit, self.buttonBox)

    def retranslateUi(self, scanOptions):
        scanOptions.setWindowTitle(_translate("scanOptions", "Scan Options", None))
        self.label_3.setText(_translate("scanOptions", "&Scan:", None))
        self.label_2.setText(_translate("scanOptions", "&Command:", None))
        self.label.setText(_translate("scanOptions", "&Target:", None))
        self.moreButton.setText(_translate("scanOptions", "More >>", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("scanOptions", "Name", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("scanOptions", "Adapter", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("scanOptions", "IP Address", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("scanOptions", "MAC Address", None))

