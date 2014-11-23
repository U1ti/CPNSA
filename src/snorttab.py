'''
Created on May 16, 2013

@author: Toshiba
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_snorttab



class view(QDialog, ui_snorttab.Ui_Form):
    
    def __init__(self,  parent=None):
        super(view, self).__init__(parent)
        self.setupUi(self)
        #header = self.tableWidget.horizontalHeader()
        #header.setStretchLastSection(True)
        self.tableWidget.setRowCount(1)
        
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = view()
    form.show()
    app.exec_()
