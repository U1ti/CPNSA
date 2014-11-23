'''
Created on Apr 16, 2013

@author: Toshiba
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_snifferView

class view(QDialog, ui_snifferView.Ui_Form):
    
    def __init__(self,  parent=None):
        super(view, self).__init__(parent)
        self.setupUi(self)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        header=self.tableView.horizontalHeader()
        header.setStretchLastSection(True)
        self.toolbar = QToolBar()
        self.gridLayout.addWidget(self.toolbar)
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = view()
    form.show()
    app.exec_()
