# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'snmp.ui'
#
# Created: Sat Jun 29 10:33:37 2013
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(631, 442)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.hostEdit = QtGui.QLineEdit(Form)
        self.hostEdit.setObjectName(_fromUtf8("hostEdit"))
        self.horizontalLayout.addWidget(self.hostEdit)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.portEdit = QtGui.QLineEdit(Form)
        self.portEdit.setObjectName(_fromUtf8("portEdit"))
        self.horizontalLayout.addWidget(self.portEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.OIDEdit = QtGui.QLineEdit(Form)
        self.OIDEdit.setObjectName(_fromUtf8("OIDEdit"))
        self.horizontalLayout_2.addWidget(self.OIDEdit)
        self.snmpWalk = QtGui.QCheckBox(Form)
        self.snmpWalk.setObjectName(_fromUtf8("snmpWalk"))
        self.horizontalLayout_2.addWidget(self.snmpWalk)
        self.startButton = QtGui.QPushButton(Form)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout_2.addWidget(self.startButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.resultBrowser = QtGui.QTextBrowser(Form)
        self.resultBrowser.setObjectName(_fromUtf8("resultBrowser"))
        self.verticalLayout.addWidget(self.resultBrowser)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Host:", None))
        self.label_2.setText(_translate("Form", "Port:", None))
        self.label_3.setText(_translate("Form", "OID", None))
        self.snmpWalk.setText(_translate("Form", "SNMP Walk", None))
        self.startButton.setText(_translate("Form", "Start", None))

