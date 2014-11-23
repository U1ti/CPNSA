#copyright to ekhumoro @ http://stackoverflow.com/questions/8332704/white-border-on-a-transparent-qsplashscreen-image-in-pyqt
#Modified by Ahmed Tantawi
from PyQt4 import QtGui, QtCore

class SplashScreen(QtGui.QWidget):
    def __init__(self, pixmap):
        QtGui.QWidget.__init__(self)
        self._pixmap = pixmap
        self._message = QtCore.QString()
        self._color = QtGui.QColor.black
        self._alignment = QtCore.Qt.AlignLeft
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setFixedSize(self._pixmap.size())
        self.setMask(self._pixmap.mask())

    def clearMessage(self):
        self._message.clear()
        self.repaint()

    def showMessage(self, message, alignment=QtCore.Qt.AlignLeft,
                                   color=QtGui.QColor.black):
        self._message = QtCore.QString(message)
        self._alignment = alignment
        self._color = color
        self.repaint()

    def paintEvent(self, event):
        textbox = QtCore.QRect(self.rect())
        textbox.setRect(textbox.x() + 5, textbox.y() + 5,
                        textbox.width() - 10, textbox.height() - 10)
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self._pixmap)
        painter.setPen(QtGui.QColor(self._color))
        painter.drawText(textbox, self._alignment, self._message)
    
if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    #show_splash('s2.gif')
    app.quit()