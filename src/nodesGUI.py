#!/usr/bin/env python


import math,os,subprocess

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Edge(QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        super(Edge, self).__init__()

        self.arrowSize = 20.0
        self.sourcePoint = QPointF()
        self.destPoint = QPointF()

        self.setAcceptedMouseButtons(Qt.NoButton)
        self.source = sourceNode
        self.dest = destNode
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.adjust()

    def type(self):
        return Edge.Type

    def sourceNode(self):
        return self.source

    def setSourceNode(self, node):
        self.source = node
        self.adjust()

    def destNode(self):
        return self.dest

    def setDestNode(self, node):
        self.dest = node
        self.adjust()

    def adjust(self):
        if not self.source or not self.dest:
            return
        
        line = QLineF(self.mapFromItem(self.source, 0, 0),
                self.mapFromItem(self.dest, 0, 0))
        length = line.length()

        self.prepareGeometryChange()
        if length > 50.0:
            edgeOffset = QPointF((line.dx() * 10) / length,
                    (line.dy() * 10) / length)

            self.sourcePoint = line.p1() + edgeOffset
            self.destPoint = line.p2() - edgeOffset
        else:
            self.sourcePoint = line.p1()
            self.destPoint = line.p1()

    def boundingRect(self):
        if not self.source or not self.dest:
            return QRectF()

        penWidth = 1.0
        extra = (penWidth + self.arrowSize) / 2.0

        return QRectF(self.sourcePoint,
                QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                        self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        if not self.source or not self.dest:
            return

        # Draw the line itself.
        line = QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine,
                Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(line)

        # Draw the arrows if there's enough room.
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = Edge.TwoPi - angle

        sourceArrowP1 = self.sourcePoint + QPointF(math.sin(angle + Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle + Edge.Pi / 3) * self.arrowSize)
        sourceArrowP2 = self.sourcePoint + QPointF(math.sin(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize);   
        destArrowP1 = self.destPoint + QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi / 3) * self.arrowSize)
        destArrowP2 = self.destPoint + QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

        painter.setBrush(Qt.black)
        painter.drawPolygon(QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
        painter.drawPolygon(QPolygonF([line.p2(), destArrowP1, destArrowP2]))


class Node(QGraphicsObject):
    Type = QGraphicsItem.UserType + 1
    doubleClickSingal = pyqtSignal(object)
    def __init__(self, graphWidget, node_dict):
        super(Node, self).__init__()
        self.graph = graphWidget
        
        self.edgeList = []
        self.newPos = QPointF()
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(1)
        self.node_dict = node_dict
    
    def getip(self):
        return self.node_dict['ip']
    def getmac(self):
        return self.node_dict['mac']
    def getosType(self):
        return  self.node_dict['osType']
    def getaccuracy(self):
        return  self.node_dict['accuracy']
    def getreason(self):
        return self.node_dict['reason']
    def getHostname(self):
        return self.node_dict['hostname']
    def getGateway(self):
        return self.node_dict['gateway']
    def getPorts(self):
        return  self.node_dict['ports']
    def type(self):
        return Node.Type
    
    def addEdge(self, edge):
        self.edgeList.append(edge)
        edge.adjust()

    def edges(self):
        return self.edgeList

    def calc(self):
        
        if not self.scene() or self.scene().mouseGrabberItem() is self:
            self.newPos = self.pos()
            return
        return
     
    def advance(self):
        return
      

    def boundingRect(self):
        return QRectF(-48,-41,100,100)

    
    def paint(self, painter, option, widget):
        textbox = QRect(-48,-41,100,100)
        if self.getGateway().strip() == self.getip():
            pix_raised = QPixmap("images/defaultGW.png")
            pix_sunken = QPixmap("images/defaultGW.png")
        elif "linux" in self.getosType().lower():
            pix_raised = QPixmap("images/LinLogo.png")
            pix_sunken =  QPixmap("images/LinLogo.png")
        elif "windows" in self.getosType().lower():
            pix_raised = QPixmap("images/WinLogo.png")
            pix_sunken = QPixmap("images/WinLogo.png")
        else:
            pix_raised = QPixmap("images/UnknownDevice.png")
            pix_sunken = QPixmap("images/UnknownDevice.png")
    
       
        if option.state & QStyle.State_Sunken:
            painter.drawPixmap(-48,-41, 96, 82, pix_raised)
            
        elif  QStyle.State_Raised:
            painter.drawPixmap(-48,-41,96 ,82, pix_raised)
        
        painter.drawText(textbox, Qt.AlignBottom|Qt.AlignCenter, self.getip())
        
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edgeList:
                edge.adjust()
            self.graph.itemMoved()

        return super(Node, self).itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
    
        super(Node, self).mousePressEvent(event)
    def mouseDoubleClickEvent(self, event):
        self.update()
        self.doubleClickSingal.emit([self.getip(),self.getmac(),self.getosType(),self.getaccuracy(),\
                                     self.getreason(),self.getHostname(),self.getPorts()])
        
       
    
    def mouseReleaseEvent(self, event):
        self.update()
        super(Node, self).mouseReleaseEvent(event)
    
class GraphWidget(QGraphicsView):
    
    MAGIC_NUMBER = 78023
    FILE_VERSION = 600

    doubleClickSig = pyqtSignal(object)
    def __init__(self,filename=QString(),  parent=None):
        super(GraphWidget, self).__init__(parent)
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.timerId = 0
        self.filename = filename
        self.modified = False
        self.xml_output = None
        self.scenez = QGraphicsScene(self)
        self.scenez.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scenez.setSceneRect(0, 0, 1024, 1024)
        self.setScene(self.scenez)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        
        self.nodeList = []
     
    def updateNode(self,data):
        self.doubleClickSig.emit(data)
    
    def loadingScreen(self):
        self.scenez.clear()
        lbl = QLabel()
        mov =  QMovie("images/loading.gif")
        lbl.setMovie(mov)
        lbl.setStyleSheet("border: 0px;background: white")
        mov.start()
        lbl.setAlignment(Qt.AlignTop)
        proxy = QGraphicsProxyWidget() 
        proxy.setWidget(lbl)
        self.scenez.addItem(proxy)
        centerz = self.mapToScene(self.rect().center())
        self.centerOn(centerz)
        proxy.setPos(256,256)
        
    def get_default_gateway(self):
        import re
        if os.name == "nt":
            cmd = ['ipconfig']
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            p = subprocess.Popen(cmd, bufsize=100000, startupinfo=startupinfo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (output, error) = p.communicate()
            output = iter(output.splitlines())
            gatewayList = []
            for line in output:
                if re.search("Default Gateway", line):
                    gatewayList.append(line)
            if not error == "":
                raise RuntimeError(error)
            tmp =""
            for i in gatewayList:
                tmp = i.split(":")
                #print tmp
                if tmp[1] != "":
                    default_gw = tmp[1]
                    break
            return default_gw
       
                
         
    
    def updateUI(self, xml_output={}):
        """Update UI i.e clear list of nodes"""
        self.nodeList = []
        self.scenez.clear()
        self.xml_output = xml_output
        self.modified = True
        rootNode = None
        firstNodeSignal = True
        drawI = 1
        tmpList = []
        default_gw = self.get_default_gateway()
        print self.xml_output
        for i in range(int(self.xml_output['status']['totalhosts'])):
            try:
                ip = xml_output['scan'].keys()[i]
            except IndexError:
                self.scale(1, 1)
                break

            if xml_output['scan'][ip]['status']['state'] == 'down':
                continue
            mac = xml_output['scan'][ip]['status']['mac']
            osType = xml_output['scan'][ip]['status']['OS']
            accuracy = xml_output['scan'][ip]['status']['accuracy']
            reason = xml_output['scan'][ip]['status']['reason']
            hostname = xml_output['scan'][ip]['hostname']   
            ports = []
            for  key in xml_output['scan'][ip]:
                if key.startswith('port'):
                    ports.append(xml_output['scan'][ip][key])
                    
         
            node_dict = {
                         'ip':ip,
                         'mac': mac,
                         'osType':osType,
                         'accuracy':accuracy,
                         'reason':reason,
                         'hostname':hostname,
                         'gateway':default_gw,
                         'ports': ports
                         }
            
            
            
            node = Node(self,node_dict)
            node.doubleClickSingal.connect(self.updateNode)

            if ip == default_gw.strip():
                self.nodeList.append(node)
            else:
                tmpList.append(node)
                
        
           
        for i in tmpList:
            self.nodeList.append(i)
            
        for node in self.nodeList:
            node.setToolTip('IP:'+node.getip()+'\nMac:'+node.getmac()+"\nOS:"+node.getosType()+'\naccuracy:'+node.getaccuracy()+"%")
            self.scenez.addItem(node)
        
            if not firstNodeSignal:
                self.scenez.addItem(Edge(rootNode, node))
            else:
                node.setPos(512,100)
                self.centerOn(node)
                rootNode=node
                firstNodeSignal= False
                continue
           
            
            
            node.setPos((drawI+50)*3, (drawI+10)*3)
            drawI+=50
        
        
        
        
        self.setAlignment(Qt.AlignTop)
        self.scale(1, 1)
        
        
    def itemMoved(self):
        if not self.timerId:
            self.timerId = self.startTimer(1000 / 25)
          
    def save(self):
        if self.filename.startsWith("new"):
            filename = QFileDialog.getSaveFileName(self,
                    "CPNSA -- Save File As", self.filename,
                    "Nbird (*.nbb *.*)")
            if filename.isEmpty():
                return
            self.filename = filename
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            stream = QDataStream(fh)
            stream.writeInt32(GraphWidget.MAGIC_NUMBER)
            stream.writeInt32(GraphWidget.FILE_VERSION)
            stream.setVersion(QDataStream.Qt_4_2)
            stream.writeQVariant((self.xml_output,))
          
            self.modified = False
        except (IOError, OSError), e:
            error = "Failed to save: %s" % e
            print error
        finally:
            if fh is not None:
                fh.close()
                return QFileInfo(self.filename).fileName()
            if exception is not None:
                raise exception
            
    def load(self):
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
        
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            
            stream = QDataStream(fh)
            magic = stream.readInt32()
            if magic != GraphWidget.MAGIC_NUMBER:
                raise IOError, "unrecognized file type"
            version = stream.readInt32()
            if version < GraphWidget.FILE_VERSION:
                raise IOError, "old and unreadable file format"
            elif version > GraphWidget.FILE_VERSION:
                raise IOError, "new and unreadable file format"
            stream.setVersion(QDataStream.Qt_4_2)
            
            xml_output = stream.readQVariant()
            self.xml_output = xml_output.toPyObject()[0]
            self.updateUI(self.xml_output)
            self.modified = False
        except (IOError, OSError), e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception
            self.modified = False
            

   
 
        
    def timerEvent(self, event):
        nodes = [item for item in self.scene().items() if isinstance(item, Node)]

        for node in nodes:
            node.calc()

        itemsMoved = False
        for node in nodes:
            if node.advance():
                itemsMoved = True

        if not itemsMoved:
            self.killTimer(self.timerId)
            self.timerId = 0

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))
    
    
    def drawBackground(self, painter, rect):
        return
        recti = QRectF(rect)
        painter.fillRect(recti, Qt.white)
        # Fill.
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(recti)
        # Text.
        textRect = QRectF(recti.left() + 0, recti.top() + 0,
                recti.width() - 0, recti.height() - 0)
        message = "CPNSA"
        font = painter.font()
        font.setBold(True)
        font.setPointSize(14)
        painter.setFont(font)
        painter.setPen(Qt.lightGray)
        painter.drawText(textRect.translated(2, 2), message)
        painter.setPen(Qt.black)
        painter.drawText(textRect, message)
    

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)
    def isModified(self):
        return self.modified
    
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    widget = GraphWidget()
    widget.showMaximized()
    widget.show()
    widget.loadingScreen()
   
    sys.exit(app.exec_())