'''
Created on Apr 25, 2013

@author: Toshiba
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class InfoTab(QTextEdit):
    '''
    classdocs
    '''
    def __init__(self,parent=None):
        '''
        Constructor
        '''
        QTextEdit.__init__(self, parent)
        self.text = 'No Scan yet'
        self.setReadOnly(True)
        self.append(self.text)
    
   
    def updateUI(self, data):
        self.clear()
        self.append('\n')
        self.cmd = '<html><u>command:</u></html> ', data['status']['cmd']
        self.append(''.join(self.cmd))
        self.down = '<html><u>downhosts:</u></html> ', data['status']['downhosts'], '\t\t  <html><u>up hosts</u></html> = ',data['status']['uphosts']
        self.append(''.join(self.down))
        self.timestr = '<html><u>Time Stamp:</u></html> ', data['status']['timestr']
        self.append(''.join(self.timestr))
        self.totalhost = '<html><u>Total hosts:</u></html> ',data['status']['totalhosts']
        self.append(''.join(self.totalhost))
        self.elapsed = '<html><u>Time elapsed:</u></html>',data['status']['elapsed']
        IPs = data['scan'].keys()
        for i in IPs:
            self.append('\n')
            self.append('--------------------------------------------------------')
            if data['scan'][i]['status']['state'] == 'down':
                self.append(i+'-- Host Down')
                continue
            self.append(i+'-- Host Up')
            self.append('<html><u>Mac:</html></u> '+data['scan'][i]['status']['mac'])
            self.append('<html><u>Mac Vendor:</html></u> '+data['scan'][i]['status']['mac_vendor'])
            self.append('<html><u>Reason:</html></u> '+data['scan'][i]['status']['reason'])
            
            
        


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = InfoTab('test')
    widget.show()
    sys.exit(app.exec_())