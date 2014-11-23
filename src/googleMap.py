

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class GMap(QWebView):
    def __init__(self, parent=None):
        super(GMap, self).__init__(parent)
        self.load(QUrl("googlemap.html"))
    
    def evalCoords(self, coords):
        
        self.frame = self.page().currentFrame()
        ltd = str(coords[0])
        lng = str(coords[1])
        datadict =  coords[2]
        send = lng+","+ltd
        
        print "addMarkerz("+send+','+'\"'+datadict+'\"'+")"
        self.frame.evaluateJavaScript(QString("addMarkerz("+send+','+'\''+datadict+'\''+")"))
       


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    browser = QWebView()
    browser.show()
    browser.load(QUrl("googlemap.html"))
    frame = browser.page().currentFrame()
  
    app.exec_()