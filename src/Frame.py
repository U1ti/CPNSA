'''
Created on Apr 12, 2013

@author: Toshiba
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import scanTab,sniffer6
import MapTab,SyslogServer,pcClient
import re,notification,snmpTab

class InnerTab(QTabWidget):
    scanTrigger = pyqtSignal(object)
    
    NextId = 1
    def __init__(self,filename=QString(), parent=None):
        super(QTabWidget, self).__init__(parent)
        #self.modified = False
        self.filename = filename
        
        if self.filename.isEmpty():
            self.filename = QString("new-{0}".format(InnerTab.NextId))
            InnerTab.NextId += 1
        #####data model
        self.notification = None
        
        self.nmap = scanTab.scanView(self.filename)
        self.addTab(self.nmap, 'Nmap')
        self.nmap.doneScanSignal.connect(self.Notify)
        self.nmap.startScanSignal.connect(self.Notify)
        
        self.sniffer= sniffer6.sniffy(self.filename)
        self.addTab(self.sniffer, 'Sniffer')
        self.sniffer.dataTrigger.connect(self.updateIPList)
        self.sniffer.startSniffSignal.connect(self.Notify)
        self.sniffer.stopSniffSignal.connect(self.Notify)
        
        self.gmap = MapTab.MapTab()
        self.addTab(self.gmap, 'Map')
        self.gmap.startLocateSingal.connect(self.Notify)
        self.gmap.finishLocateSignal.connect(self.Notify)
        
        self.Syslog = SyslogServer.udpServer()
        self.addTab(self.Syslog, 'Syslog')
        self.Syslog.alertSignal.connect(self.notifyCell)
        
        self.snmp =  snmpTab.SnmpTab()
        self.addTab(self.snmp, 'Snmp')
        
        """
        self.pcclient = pcClient.Client()
        self.addTab(self.pcclient,'remote')
        """        
        self.setWindowTitle(QFileInfo(self.filename).fileName())
    
    def notifyCell(self, data ):
        self.pcclient.Notfiy(data)

    def Notify(self, mssg):
        self.notification = None
        self.notification = notification.Notification(mssg)
        self.notification.show()
        self.notification.setFocus()
    
    def closeAll(self):
        self.nmap.stopScan()
             
    def closeEvent(self, event):
        
        if (self.isModified() and 
            QMessageBox.question(self,
                   "CPNSA - Unsaved Changes",
                   "Save unsaved changes in {0}?".format(self.filename),
                   QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.Yes):
            try:
                self.save()
            except (IOError, OSError), e:
                QMessageBox.warning(self,
                        "CPNSA -- Save Error",
                        "Failed to save {0}: {1}".format(self.filename, e)) 
        #self.close()
        if self.notification is not None:
            self.notification.close()
    
    def isvalid(self,IP):
        tmp = re.search(r'(^127\.0\.0\.1)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)|(^22[4-9]\.)|(^23[3-9]\.)',str(IP))
        if tmp:
            return False
        return True
        
    def updateIPList(self,IP):
        if self.isvalid(IP[0]) or self.isvalid(IP[1]):
            item = QListWidgetItem(IP[0]+" -> "+IP[1])
            self.gmap.IPlist.addItem(item)
        
            
    
    def save(self):
        if self.nmap.isModified():
            self.nmap.save()
        if self.sniffer.isModified():
            self.sniffer.save()
        
        #self.modified = False
    def load(self):
        self.nmap.load()
        #self.modified = False
    
    def isModified(self):
        if self.nmap.isModified() or self.sniffer.isModified():
            return True
        return False
   

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    form = InnerTab()
    
    form.show()
    dev = '{AC0E7349-B861-4459-AFF7-AB371F31339F}'
   
    
    app.exec_()
