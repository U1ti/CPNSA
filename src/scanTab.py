#!/usr/bin/python

'''
Created on Apr 24, 2013

@author: Toshiba
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import nodesGUI,nmap_glue,scanViewInfoTab,scanOptionsDlg


class nmap_thread(QThread):
    """Class to run a  different thread for nmap"""
    
    """A signal to return with either the output or the error"""
    xml_signal = pyqtSignal(object)

    def __init__(self,cmd):
        QThread.__init__(self)
        """
        command sent from the UI
        """
        self.cmd = cmd
        self.nmapInstance = nmap_glue.nmapGlueClass()
       
    def run(self):
        """
        Method that sends command to nmap.
        If there are any errors in the command or the target, sends back an exception.
        """
        self.SCAN_STOPPED = False
        try:
            self.xml_output= self.nmapInstance.nmapScan(self.cmd)
        except Exception as e:
            if self.SCAN_STOPPED:
                self.xml_signal.emit(self.SCAN_STOPPED)
                return
            self.xml_signal.emit(e)
            return
        
        self.xml_signal.emit(self.xml_output)
    def stop(self):
        self.SCAN_STOPPED= True
        self.nmapInstance.stopScan()
        

class scanView(QWidget):
    """GUI interface Class"""
    
    doneScanSignal = pyqtSignal(object)
    startScanSignal = pyqtSignal(object)
    def __init__(self, filename, parent=None): 
        QWidget.__init__(self, parent)
        self.filename = filename
        
        splitter= QSplitter(Qt.Vertical)
        splitter.resize(100,200)
        
        self.grapWid =  nodesGUI.GraphWidget(self.filename,parent=splitter)
        self.grapWid.doubleClickSig.connect(self.updateHostTab)
        self.tabWid = QTabWidget(splitter)
        
        self.scanInfo = scanViewInfoTab.InfoTab()
        self.tabWid.addTab(self.scanInfo, 'General Info')
        
        self.hostInfo = QTextEdit()
        self.hostInfo.setReadOnly(True)
        self.tabWid.addTab(self.hostInfo, 'Host Info')
        
        self.scanButton = QPushButton("Start Scan")
        self.scanButton.clicked.connect(self.startScan)
        
        self.stopButton = QPushButton("Stop Scan")
        self.stopButton.clicked.connect(self.stopScan)
        self.stopButton.setDisabled(True)
        
        self.savePNGButton = QPushButton("Save as png")
        self.savePNGButton.clicked.connect(self.savePNG)
        self.savePNGButton.setDisabled(True)
        
        self.savePDFbutton = QPushButton("Save pdf")
        self.savePDFbutton.clicked.connect(self.savePDF)
        self.savePDFbutton.setDisabled(True)
        
        self.savePrinterButton = QPushButton("Print")
        self.savePrinterButton.clicked.connect(self.savePrinter)
        self.savePrinterButton.setDisabled(True)
       
        self.toolbar = QToolBar()
        self.toolbar.addWidget(self.scanButton)
        self.toolbar.addWidget(self.stopButton)
        self.toolbar.addWidget(self.savePNGButton)
        self.toolbar.addWidget(self.savePDFbutton)
        self.toolbar.addWidget(self.savePrinterButton)
        
        self.thread =None
        splitter.setSizes([300,200])
        
        gridbox = QGridLayout()
        gridbox.addWidget(splitter)
        gridbox.addWidget(self.toolbar)
        self.setLayout(gridbox)
        
        self.tmp = []
    def updateHostTab(self,data):
        self.tabWid.setCurrentIndex(1)
        #self.hostInfo.setFocus()
        self.hostInfo.clear()
        #print data
        self.hostInfo.append('<html><b>IP: </b></html>'+data[0])
        self.hostInfo.append('<html><b>Mac: </b></html>'+data[1])
        self.hostInfo.append('<html><b>OS: </b></html>'+data[2]+' ,Accuracy='+data[3]+"%")
        self.hostInfo.append('<html><b>Reason: </b></html>'+data[4])
        if  data[5] != "":
            self.hostInfo.append('<html><b>Hostname: </b></html>'+data[5])
        for item in data[6]:
            self.hostInfo.append('-------------------------------------')
            for key in item:
                self.hostInfo.append(key+':    '+str(item[key]))
                
        
         
    def isModified(self):
        return self.grapWid.isModified()
    
    def load(self):
        self.grapWid.load()
    
    def savePNG(self):
        
        out = QPixmap(2000,2000)
        self.tmp.append(out)
        paint = QPainter(out)
        self.tmp.append(paint)
        
        targ = QRectF(0,0,2000,2000)
        src = QRect(0,0,2000,2000)
        paint.fillRect(targ, Qt.white)
        self.grapWid.render(paint,targ,src)
      
        
        out.save(self.filename+".png", "PNG")
    
    
    def saveDialog(self):
        filename = QFileDialog.getSaveFileName(self,
                "CPNSA -- Save File As", '*.pdf',
                "pdf (*.pdf *.*)")
        return filename
            
    def savePrinter(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.scanInfo.print_)
        dialog.exec_()

    def savePDF(self):
        filename = self.saveDialog()
        if filename.isEmpty():
            return
        printer = QPrinter()
        printer.setPageSize(QPrinter.Letter)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(filename)
        
        self.scanInfo.print_(printer)
        
    
    def startScan(self):
        scanDlg = scanOptionsDlg.scanOptions()
        self.thread =None
        if scanDlg.exec_():
            self.grapWid.loadingScreen()
            self.scanButton.setDisabled(True)
            self.stopButton.setDisabled(False)
            self.savePNGButton.setDisabled(True)
            self.savePDFbutton.setDisabled(True)
            self.savePrinterButton.setDisabled(True)
            
            self.startScanSignal.emit("Scanning has started")
            self.threads = []
            self.thread = nmap_thread(scanDlg.getCMD())
            self.thread.xml_signal.connect(self.ready)
            self.thread.start()
            self.threads.append(self.thread)
        
    
    def save(self):
        self.grapWid.save()
    
    def updateUI(self,xml_output):
        
        self.grapWid.updateUI(xml_output)
        self.doneScanSignal.emit("Scanning has finished")
        
        self.scanInfo.updateUI(xml_output)
        self.scanButton.setDisabled(False)
        self.stopButton.setDisabled(True)
        self.savePNGButton.setDisabled(False)
        self.savePDFbutton.setDisabled(False)
        self.savePrinterButton.setDisabled(False)
        
    def get_target_items(self):
        return self.grapWid.nodeList
    
    def stopScan(self):
        if self.thread is not None:
            self.thread.stop()
    
  
      
    def loadingScreen(self):
        self.grapWid.loadingScreen()
      
    def ready(self, data):
        if isinstance(data, bool):
            QMessageBox.information(self, 'Info', 'You have stopped scan!')
            self.grapWid.scenez.clear()
            self.scanButton.setDisabled(False)
            self.stopButton.setDisabled(True)
            self.savePNGButton.setDisabled(True)
            self.savePDFbutton.setDisabled(True)
            self.savePrinterButton.setDisabled(True)
            
            self.grapWid.modified = False
            return
        if isinstance(data, Exception):
            self.scanButton.setDisabled(False)
            self.stopButton.setDisabled(True)
            self.savePNGButton.setDisabled(True)
            self.savePDFbutton.setDisabled(True)
            self.savePrinterButton.setDisabled(True)
            self.grapWid.scenez.clear()
            
            QMessageBox.critical(self, 'Error',str(data))
            return   
        self.updateUI(data)
        


        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = scanView('test')
    widget.show()
    sys.exit(app.exec_())