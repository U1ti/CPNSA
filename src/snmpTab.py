'''
Created on June 17, 2013

@author: Toshiba
'''
import sys, snmp2, snmpGUI
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class SnmpTab(QWidget):

    def __init__(self):
        QWidget.__init__(self )
        self.snmpView = snmpGUI.view()
        self.snmpMan = snmp2.SNMPManager()
        layout = QGridLayout()
        layout.addWidget(self.snmpView)
        self.setLayout(layout)
        self.snmpView.startButton.clicked.connect(self.populate)
        
    def populate(self):
        ip = str(self.snmpView.hostEdit.text())
        port = int(self.snmpView.portEdit.text())
        OID = self.snmpView.OIDEdit.text()
        
        if ip == "":
            ip = '127.0.0.1'
        if port == "":
            port = 161
        if self.snmpView.snmpWalk.checkState() ==  Qt.Checked:
            OID = '.1.3.6.1'
        elif OID == "":
            QMessageBox.critical(self, 'Error',"You have to specify an OID or choose snmp walk ")
            return
        
            
        try:
            self.snmpView.resultBrowser.clear()    
            output  = self.snmpMan.requestSNMP(ip,port,OID)
            for key in output:
                self.snmpView.resultBrowser.append('.'.join(output[key][0])+"   ="+output[key][1])
        except Exception as e:
            QMessageBox.critical(self,'Error',str(e))
            return
        

   
        
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = SnmpTab()
    window.show()
    sys.exit(app.exec_())