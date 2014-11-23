#!/usr/bin/python

import sys,snifferView,snifferDlg

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from struct import *
import pcapy,os
from pcapy import findalldevs, open_live
import impacket,snifferModel
from impacket.ImpactDecoder import EthDecoder, LinuxSLLDecoder
from impacket.ImpactPacket import IP, TCP, UDP, ICMP, ARP, IGMP
MAX_LEN      = 1518   

READ_TIMEOUT = 100     
PCAP_FILTER  = ''      

class DecoderThread(QThread):
    trigger = pyqtSignal(object)
    def __init__(self, pcapObj, filename, parent=None):
        QThread.__init__(self, parent)
        
        datalink = pcapObj.datalink()
        self.filename = filename
        self.exitFlag=False
        
        self._current_bytes_rate = 0
        self.total_transfer = 0 
        self._tmp_bytes_per_sec_sum = 0 
        self._inc = 0 
        self._dispatch_bytes_sum = 0 

        if pcapy.DLT_EN10MB == datalink:
            self.decoder = EthDecoder()
        elif pcapy.DLT_LINUX_SLL == datalink:
            self.decoder = LinuxSLLDecoder()
        else:
            raise Exception("Datalink type not supported: " % datalink)
        self.pcap = pcapObj
        self.dumper = self.pcap.dump_open(str(self.filename+".tmp"))
    
    def run(self):
      
        self.pcap.loop(0, self.packetHandler)
        
    def stop(self):
        self.exitFlag = True
        
        
    def packetHandler(self, hdr, data):
       
        self._dispatch_bytes_sum += len(data) 

        if self.exitFlag:
            try:
                self.dumper = ""
                self.pcap.BREAK_LOOP()
            except:
                return
        self.dumper.dump(hdr, data)
        self.trigger.emit(self.decoder.decode(data))
        
class sniffy(QWidget):
    
    dataTrigger = pyqtSignal(object)
    
    startSniffSignal = pyqtSignal(object)
    stopSniffSignal = pyqtSignal(object)
    
    def __init__(self,filename=QString(), parent=None ,**kwargs): 
        QWidget.__init__(self, parent,**kwargs) 
        layout = QVBoxLayout(self)
        self.lv = snifferView.view()
        layout.addWidget(self.lv) 
        self.setLayout(layout)
        # layout
        self.proxy = QSortFilterProxyModel()
        headers = ['No','Source','Destination','Protocol']
        
        self.filename = filename
        
        self.model = snifferModel.tableModel(headers=headers)
        self.lv.tableView.setModel(self.proxy)
        self.proxy.setSourceModel(self.model)
        self.modified = False
        self.resultList = []
       
        self.hexDump = ''
        self.count = 0
        
        self.lv.filterEdit.returnPressed.connect(self.makeChoice)
        self.selected = False
        self.lv.tableView.selectionModel().selectionChanged.connect(self.rowSelected)
        
        
        self.sniffButton = QPushButton("Sniff")
        self.sniffButton.clicked.connect(self.startSniff)
        self.stopButton = QPushButton("Stop Sniffing")
        self.stopButton.clicked.connect(self.stopSniff)
        self.stopButton.setDisabled(True)
        self.lv.toolbar.addWidget(self.sniffButton)
        self.lv.toolbar.addWidget(self.stopButton)
    
    def makeChoice(self):
        
        if self.lv.filterEdit.text() == "":
            self.proxy.setFilterFixedString("")
            return
        
        filter=str(self.lv.filterEdit.text()).split('=')
       
        if filter[0].lower() ==  'source' or\
           filter[0].lower() == 'src':
            col_num = 1
        
        elif filter[0].lower() == 'destination' or\
             filter[0].lower() == 'dst':
            col_num = 2
       
        elif filter[0].lower() == 'protocol':
            col_num = 3
            filter[1] = filter[1].upper()
        
        else:
            QMessageBox.warning(self,
                    "CPNSA  -- Filter Error",
                    "No such filter. Please check Help. ")
            return
        
        self.proxy.setFilterFixedString(filter[1])
        self.proxy.setFilterKeyColumn(col_num)
    
    def rowSelected(self):
        index = self.lv.tableView.currentIndex()
        self.lv.dataEdit.clear()
        self.lv.dataEdit.append(self.resultList[index.row()])
    
    
    def getInterface(self):
        devs = findalldevs()
        if 0 == len(devs):
            raise RuntimeError("No interfaces found to select.\nHint:You don't have enough permissions to open any interface on this system.")
            sys.exit(1)
        return devs
    
    def str2mac(self, mac):
        return "%02x:%02x:%02x:%02x:%02x:%02x" % unpack("!6B",mac)
    
    def startSniff(self):
        sniffDlg =  snifferDlg.view()
        sniffDlg.updateUI()
        
        if sniffDlg.exec_():
            checked,dev=sniffDlg.getArgs()
            self.stopButton.setDisabled(False)
            self.sniffButton.setDisabled(True)
            self.startSniffSignal.emit("Sniffing has started")
            self.model.resetModel()
            self.count = 0
            self.modified = True
            
            filter = ''
         
            if checked == Qt.Checked:
                promisc = 1
            else:promisc = 0
       
            if os.name == 'nt':
                dev = '\Device\NPF_'+dev
            try:
                p = open_live(str(dev), MAX_LEN, promisc, 100)
            except Exception as e:
                QMessageBox.critical(self,"Error", "Promiscous Mode not supported by your NIC!")
                self.stopButton.setDisabled(True)
                self.sniffButton.setDisabled(False)
                return
            p.setfilter(filter)
            print "Listening on %s: net=%s, mask=%s, linktype=%d" % (dev, p.getnet(), p.getmask(), p.datalink())
            self.threads = []    
            self.thread = DecoderThread(p,self.filename)
            self.thread.start()
            self.thread.trigger.connect(self.updateUi) 
            self.threads.append(self.thread) # keep a reference
            
    def stopSniff(self):
        self.thread.stop()
        self.stopButton.setDisabled(True)
        self.sniffButton.setDisabled(False)
        self.stopSniffSignal.emit("Sniffing has stopped")
        
    def isModified(self):
        return self.modified   
    
    def save(self):
        if self.filename.startsWith("new"):
            new_filename = QFileDialog.getSaveFileName(self,
                    "Nbird -- Save File As", self.filename,
                    "pcap (*.pcap *.*)")
            if new_filename.isEmpty():
                return
            self.new_filename = new_filename
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        exception = None
        try:
            os.rename(self.filename+".tmp", self.new_filename)
            
        except (OSError), e:
            error = "Failed to save: %s" % e
            print error
        finally:
            if exception is not None:
                raise exception
    
    
    def updateUi(self,data):
        ip_hdr = data.child()
        tcp_hdr = ip_hdr.child()
        
        source_mac = data.get_ether_shost()
        dest_mac = data.get_ether_dhost()
        protocol = ""
        source_mac = self.str2mac(source_mac)
        dest_mac = self.str2mac(dest_mac)
        try:
            protocol_id = data.child().child().protocol
        except:
            print ip_hdr

        
        try:
            ip_hdr.child().child()
            
            self.hexDump = str(data)
        except:
           
            self.hexDump =str(data)
        
        
        if isinstance(ip_hdr, ARP):
         
            protocol =  'ARP'
            src = source_mac
            dst = dest_mac
            
        else:
            src = ip_hdr.get_ip_src()
            dst = ip_hdr.get_ip_dst()
        
        if isinstance(tcp_hdr, TCP):
            protocol =  'TCP'
            srcport= ip_hdr.child().get_th_sport()
            dstport= ip_hdr.child().get_th_dport()
            
            
        elif isinstance(tcp_hdr, ICMP):
            protocol = 'ICMP'
         
        elif isinstance(tcp_hdr, UDP):
            protocol = "UDP"
       
        elif protocol != 'ARP':
            protocol = "IGMP"
        row = [self.count,src,dst,protocol]
        self.model.insertRows(self.count,self.count,row)
        
      
        self.dataTrigger.emit([src,dst])
        self.resultList.append(self.hexDump)
        self.count+=1
        
   


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = sniffy()
    form.show()
    form.startSniff(1,'{AC0E7349-B861-4459-AFF7-AB371F31339F}')
    app.exec_()

