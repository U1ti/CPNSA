'''
Created on Apr 4, 2013

@author: Toshiba
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

import ui_scanOptions

INTENSE_SCAN = 0
INTENSE_UDP = 1
INTENSE_ALL_TCP = 2
INTENSE_NO_PING = 3
PING_SCAN = 4
QUICK_SCAN = 5
QUICK_SCAN_PLUS = 6
QUICK_TRACEROUTE = 7
REGULAR_SCAN = 8
SLOW_SCAN = 9


class scanOptions(QDialog,ui_scanOptions.Ui_scanOptions):
    
    scan_types = ['Intense Scan','Intense scan plus UDP','Intense scan, all TCP ports','Intense scan, no ping','Ping scan'\
                  ,'Quick Scan', 'Quick Scan Plus', 'Quick traceroute', 'Regular Scan']
    
    def __init__(self,  parent=None):
        super(scanOptions, self).__init__(parent)
        self.setupUi(self)
        self.moreFrame.hide()

        self.connect(self.comboBox,SIGNAL("currentIndexChanged(QString)"),self.comboBoxUpdate)
        self.connect(self.targetEdit,SIGNAL("textEdited(QString)"),self.targetEditUpdate)
        self.connect(self.commandEdit,SIGNAL("textEdited(QString)"),self.commandEditUpdate)
        self.comboBox.addItems(self.scan_types)
        self.ip = ""
        self.count = 0
        self.getInterface()
        
    def getInterface(self):
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
   
    def accept(self):
        QDialog.accept(self)
    
    def getCMD(self):
        return str(self.commandEdit.text())
   
    def comboBoxUpdate(self):
        self.choice = getChoice(self.comboBox.currentIndex())
        self.commandEdit.setText(self.choice)
        self.cmd = self.commandEdit.text()
       
    def targetEditUpdate(self):
        self.commandEdit.setText(self.cmd.remove(self.ip)+self.targetEdit.text())
            
        
    def commandEditUpdate(self):
        self.cursorPos = self.commandEdit.cursorPosition()
        self.cmd = self.commandEdit.text()
        temp=self.cmd.split(' ')
        self.ip = temp[len(temp)-1]
        self.targetEdit.setText(self.ip)
        self.commandEdit.setCursorPosition(self.cursorPos)
       
  
def getChoice(choice):
    if choice == INTENSE_SCAN:
        return 'nmap -T4 -A -v '
    elif choice == INTENSE_UDP:
        return 'nmap -sS -sU -T4 -A -v '
    elif choice == INTENSE_ALL_TCP:
        return 'nmap -p 1-65535 -T4 -A -v '
    elif choice == INTENSE_NO_PING:
        return 'nmap -T4 -A -v -Pn '
    elif choice == PING_SCAN:
        return 'nmap -sn '
    elif choice == QUICK_SCAN:
        return 'nmap -T4 -F '
    elif choice == QUICK_SCAN_PLUS:
        return 'nmap -sV -T4 -O -F --version-light '
    elif choice == QUICK_TRACEROUTE:
        return 'nmap -sn --traceroute '
    elif choice == REGULAR_SCAN:
        return 'nmap '
    
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    form = scanOptions()
    form.show()
    app.exec_()
