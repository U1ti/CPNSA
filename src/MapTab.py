'''
Created on May 6, 2013
@author: Toshiba
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import googleMap,urllib2,json,re

        
        
        
class MapTab(QWidget):
    startLocateSingal = pyqtSignal(object)
    finishLocateSignal = pyqtSignal(object)
    def __init__(self,  parent=None): 
        QWidget.__init__(self, parent)
        self.api = 'f7f00323fb6537d1b069729d6152e1a91a04e2a3961d1cf60441ac9d5f4e1c9a'
        
        self.gmap = googleMap.GMap()
        self.gmap.setMinimumWidth(900)
        
        self.IPlist = QListWidget()
        self.IPlist.doubleClicked.connect(self.traceIP)
        self.IPlist.setMaximumWidth(300)
        
        
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.IPlist)
       
        rightWidget = QWidget()
        rightWidget.setLayout(rightLayout)
        
        splitter =  QSplitter(Qt.Horizontal)
        splitter.addWidget(self.gmap)
        splitter.addWidget(rightWidget)
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,0)
        
        gridbox = QGridLayout()
        gridbox.addWidget(splitter,0,0)
        
        self.setLayout(gridbox)    
     
     
    def unmarkAllFn(self):
        pass   
    def markAllFn(self):
        pass
    def isvalid(self,IP):
        tmp = re.search(r'(^127\.0\.0\.1)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)|(^22[4-9]\.)|(^23[3-9]\.)',str(IP))
        
        if tmp:
            return False
        return True
        
    def traceIP(self):
        self.startLocateSingal.emit("Geolocating IP..")
        ip = self.IPlist.currentItem().text()
        ip =ip.split('->')
        if self.isvalid(ip[0]):
            ip = ip[0]
            
        elif self.isvalid(ip[1]):
            ip = ip[1]
        
        
        url = "http://api.ipinfodb.com/v2/ip_query.php?timezone=true&output=json&key="+self.api\
        +"&ip="+str(ip).strip()
        urlobj = urllib2.urlopen(str(url))
        
        data = urlobj.read()
        
        urlobj.close()
        datadict = json.loads(data)
        dictIP = "IP: "+str(datadict['Ip'])+"<br>"
        dictZone="Time Zone:"+str(datadict['TimezoneName'])+"<br>"
        dictZip = "Zip Code: "+str(datadict['ZipPostalCode'])+"<br>"
        dictCity = "City: "+str(datadict['City'])+"<br>"
        dictRegion = "Region:"+str(datadict['RegionName'])+"<br>"
        dictCountry = "Country:"+str(datadict['CountryName'])+"<br>"
        info = dictIP+dictCity+dictRegion+dictCountry
        
        
        
        self.gmap.evalCoords([datadict['Longitude'],datadict['Latitude'],info]) 
        self.finishLocateSignal.emit("Finished Gelocating..")



if __name__ == '__main__':
    import sys,snifferModel
    app = QApplication(sys.argv)
    model = snifferModel.tableModel()
    widget = MapTab(model)
    widget.show()
    sys.exit(app.exec_())