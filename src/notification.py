###############################
#                             #
#  Coded By: Saurabh Joshi    #
#  Modified By: Ahmed Tantawi #
#  Original: 12/10/12         #
#  Date Modified: 8/12/12     #
#                             #
#  File: Notification System  #
###############################

import sys
from PyQt4 import QtCore, QtGui

import time

MSSG = ''

from ui_notification import Ui_Notification

class Notification(QtGui.QMainWindow):
    closed = QtCore.pyqtSignal()
    
    def __init__(self,mssg,parent=None):
        QtGui.QWidget.__init__(self,parent,QtCore.Qt.WindowStaysOnTopHint)
        self.parent = parent
        global MSSG
        MSSG = mssg
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui = Ui_Notification()
        self.ui.setupUi(self)
        
        self.createNotification(MSSG)
        
    def createNotification(self,mssg):
        
        cp = QtGui.QDesktopWidget().availableGeometry()
        self.x = cp.width()
        self.y = cp.height()

        #Set the opacity
        self.f = 1.0

        #Set the message 
        self.ui.lbl_mssg.setText(mssg)

        #Start Worker
        self.workThread = WorkThread()
        self.connect( self.workThread, QtCore.SIGNAL("update(QString)"), self.animate )
        self.connect( self.workThread, QtCore.SIGNAL("vanish(QString)"), self.disappear)
        self.connect( self.workThread, QtCore.SIGNAL("finished()"), self.done)
        
        self.workThread.start()
        return

    #Quit when done
    def done(self):
        self.hide()
        return

    #Reduce opacity of the window
    def disappear(self):
        self.f -= 0.01
        self.setWindowOpacity(self.f)
        return
        
        
    #Move in animation
    def animate(self):
        self.move(self.x,self.y)
        self.x -= 1
        self.y -= 0.17
        return
        
        

#The Worker
class WorkThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        #Bring
        for i in range(336):
            time.sleep(0.0001)
            self.emit( QtCore.SIGNAL('update(QString)'), "ping" )
        #Hide
        for j in range(50):
            time.sleep(0.1)
            self.emit( QtCore.SIGNAL('vanish(QString)'), "ping" )
        return
def Notify(msg):
    app = QtGui.QApplication(sys.argv)
    myapp = Notification(msg)
    myapp.show()
    sys.exit(app.exec_())

     

        
        
        
