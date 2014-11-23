'''
Created on Jul 1, 2013

@author: Toshiba
'''
from PyQt4 import  QtNetwork
from PyQt4.QtCore import *
from PyQt4.QtGui import *
cellPort=6666
serverport= 9407
SIZEOF_UINT16 = 2
class Cell(QDialog):
    def __init__(self, parent=None):
        super(Cell, self).__init__(parent)
        self.nextBlockSize = 0
        self.serverAddress='localhost'
        self.socket = QtNetwork.QTcpSocket()
        self.connect(self.socket, SIGNAL("connected()"), self.sendRequest)
        self.connect(self.socket, SIGNAL("readyRead()"), self.readResponse)
        self.connect(self.socket, SIGNAL("disconnected()"),
                     self.serverHasStopped)
        self.connect(self.socket,
                     SIGNAL("error(QAbstractSocket::SocketError)"),
                     self.serverHasError)
        self.passwordEdit = QLineEdit()
        self.usernameEdit = QLineEdit()
        
        layout = QGridLayout()
        self.passwordEdit.returnPressed.connect(self.grab)
        layout.addWidget(self.usernameEdit)
        layout.addWidget(self.passwordEdit)
        self.setLayout(layout)
        
        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.udpSocket.bind(cellPort)
        self.udpSocket.readyRead.connect(self.processPendingDatagrams)
        

    def processPendingDatagrams(self):
            """receive and decode multicast messages and send a response message on the return address"""
    
            while self.udpSocket.hasPendingDatagrams():
                datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
                self.statusLabel.setText("received mcast msg '%s'" % datagram)
                # send a response back to msend 
                self.answerSocket.writeDatagram("hi back", Q(self.answerAddress), answer_port)
        
    def sendRequest(self):
            print "Sending request..."
            self.socket.write(self.request)
            self.request = None 
    
    def grab(self):
        self.issueRequest(QString("grab"), self.usernameEdit.text(),
                          self.passwordEdit.text())

    def readResponse(self):
        stream = QDataStream(self.socket)
        stream.setVersion(QDataStream.Qt_4_2)

        while True:
            
            if self.nextBlockSize == 0:
                if self.socket.bytesAvailable() < SIZEOF_UINT16:
                    
                    break
                self.nextBlockSize = stream.readUInt16()
            if self.socket.bytesAvailable() < self.nextBlockSize:
                
                break
            
            action = QString()
            computer = QString()
            port = QString()
            stream >> action >> computer >> port
            
            msg = QString()
            
            if action == "ERROR":
                msg = QString("Error: %1").arg(computer)
            elif action == "grab":
                msg = "IP="+computer+"Port="+port
            print(msg)
            
            self.nextBlockSize = 0


    def serverHasStopped(self):
        print("Error: Connection closed by server")
        self.socket.close()


    def serverHasError(self, error):
        print(QString("Error: %1").arg(self.socket.errorString()))
        self.socket.close()
    
    def issueRequest(self, action, computer, password):
        self.request = QByteArray()
        stream = QDataStream(self.request, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        stream.writeUInt16(0)
        stream << QString(action) << QString(computer) << QString(password)
        stream.device().seek(0)
        stream.writeUInt16(self.request.size() - SIZEOF_UINT16)
        if self.socket.isOpen():
            self.socket.close()
        print "Connecting to server..."
        self.socket.connectToHost("localhost", serverport)


   
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = Cell()
    form.show()
    app.exec_()

