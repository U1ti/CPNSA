
'''
Created on Apr 16, 2013

@author: Ahmed Tantawi
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import ui_sniffDlg

class view(QDialog, ui_sniffDlg.Ui_Dialog):
    
    def __init__(self,  parent=None):
        super(view, self).__init__(parent)
        self.setupUi(self)
        self.count = 0
        
    def getArgs(self):
        index = self.tableWidget.currentRow()
        print self.checkPromisc.checkState(), self.tableWidget.item(index, 1).text()
        return self.checkPromisc.checkState(),self.tableWidget.item(index, 1).text()

    def updateUI(self):
        interface = QNetworkInterface()
        allInter = interface.allInterfaces()
        for i in allInter:
            interfaceFlags = i.flags()
            if interfaceFlags & QNetworkInterface.IsUp and interfaceFlags & QNetworkInterface.IsRunning \
                    and interfaceFlags & QNetworkInterface.CanBroadcast  \
                    and not interfaceFlags & QNetworkInterface.IsLoopBack:
                        name = QTableWidgetItem(i.name())
                        mac =QTableWidgetItem(i.hardwareAddress())
                        humanReadable= QTableWidgetItem(i.humanReadableName())
                        entry = i.addressEntries()
                        ip= QTableWidgetItem(entry[1].ip().toString())
                      
                        self.tableWidget.setItem(self.count,0,humanReadable)
                        self.tableWidget.setItem(self.count,1,name)
                        self.tableWidget.setItem(self.count,2,ip)
                        self.tableWidget.setItem(self.count,3,mac)
                        self.count+=1
                        self.tableWidget.insertRow(self.count)
        self.tableWidget.removeRow(self.count)
                        
            
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = view()
    form.show()
    form.updateUI()
    form.getArgs()
    
    app.exec_()
