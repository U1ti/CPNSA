
'''
Created on Apr 16, 2013

@author: Toshiba
'''
from socket import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import snorttab
import datetime


class snort_server_thread(QThread):
    """Thread to keep listening to snort client alerts"""

    messageSignal = pyqtSignal(object)
    socketErrorSignal = pyqtSignal(object)
    
    def __init__(self, IP, port):
        QThread.__init__(self)
        self.IP = IP
        self.port = port
        self.server_socket = None
        
       
    def run(self):
        address = (self.IP, self.port)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)

        try:
            self.server_socket.bind(address)
        except Exception as e:
            self.socketErrorSignal.emit("Make sure the port is not binded.")
            return
        while(1):
            try:
                
                recv_data, addr = self.server_socket.recvfrom(2048)
                self.messageSignal.emit([recv_data,addr])
            except Exception as e:
                raise Exception('boom')
                return
    
    def stop(self):
        self.server_socket.shutdown(1)
        self.server_socket.close()
        
        
class udpServer(QWidget):
    """UDP Syslog server class for snort client"""
    alertSignal = pyqtSignal(object)
    def __init__(self, IP=None, port=None, parent=None):
        QWidget.__init__(self, parent)
        self.IP = IP
        self.port = port
        self.snort = snorttab.view()
        gridbox = QGridLayout()
        gridbox.addWidget(self.snort)
        self.setLayout(gridbox)
        self.count = 0
        self.syslogStartedFLAG = False
        self.snort.syslogButton.clicked.connect(self.startSyslog)
        
        
    def startSyslog(self):
        """Start Syslog server to listen to specified IP address & port."""
        
        if self.syslogStartedFLAG:
            #if syslogstarted flag is true then stop syslog server
            self.stopSyslog()
            self.syslogStartedFLAG = False
            return
            
        if self.snort.hostnameEdit.text() == "" and self.snort.portEdit.text() == "":
            self.IP = '127.0.0.1'
            self.port = 514
        else:
            self.IP = self.snort.hostnameEdit.text()
            self.port = int(self.snort.portEdit.text())

        self.threads = []    
        self.thread = snort_server_thread(self.IP, self.port)
        self.thread.socketErrorSignal.connect(self.SocketError)
        try:
            self.thread.start()
            
        except Exception as e:
            QMessageBox.critical(self,'error', error)
        self.thread.messageSignal.connect(self.updateUi) 
        self.threads.append(self.thread) # keep a reference
        self.snort.syslogButton.setText('Stop Syslog')
        self.syslogStartedFLAG = True
    
    def SocketError(self,error):
        QMessageBox.critical(self,'error',error)
    def stopSyslog(self):
        """stops snort thread by triggering stop method in thread class"""
        
        self.thread.stop()
        self.snort.syslogButton.setText('Start Syslog')
        
    
    def updateUi(self, alert):
        """Handle updates to the UI when a new alert is recieved"""
        
        time = datetime.datetime.now()
        self.alertSignal.emit(alert[0])
        message = QTableWidgetItem(alert[0])
        message.setTextAlignment(Qt.AlignHCenter)
        
        hostname = QTableWidgetItem(alert[1][0])
        hostname.setTextAlignment(Qt.AlignHCenter)
        
        date = QTableWidgetItem(time.strftime("%Y-%m-%d"))
        date.setTextAlignment(Qt.AlignHCenter)
        
        time = QTableWidgetItem(time.strftime("%H:%M"))
        time.setTextAlignment(Qt.AlignHCenter)
       
        self.snort.tableWidget.setItem(self.count, 0, time)
        self.snort.tableWidget.setItem(self.count, 1, date)
        self.snort.tableWidget.setItem(self.count, 2, hostname)
        self.snort.tableWidget.setItem(self.count, 3, message)
        
        self.snort.tableWidget.resizeColumnsToContents()
        
        self.count+=1
        self.snort.tableWidget.insertRow(self.count)
        
        
        
        
if __name__ == '__main__':
    """test syslog server"""
    import sys

    app = QApplication(sys.argv)
    widget = udpServer()
    #widget.startSyslog()
    widget.show()
    
    sys.exit(app.exec_())
        