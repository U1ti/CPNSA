#copyright http://www.diotavelli.net/PyQtWiki/Movie%20splash%20screen
#Modified by Ahmed Tantawi

import sys, time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class IntroSplashScreen(QSplashScreen):

    def __init__(self, splash_gif, parent = None):
        splash_gif.jumpToFrame(0)
        pixmap = QPixmap(splash_gif.frameRect().size())
        QSplashScreen.__init__(self, pixmap)
        self.splash_gif = splash_gif
        self.splash_gif.frameChanged.connect(self.repaint)
    
    def showEvent(self, event):
        self.splash_gif.start()
    
    def hideEvent(self, event):
        self.splash_gif.stop()
    
    def paintEvent(self, event):
        textbox = QRect(self.rect())
        textbox.setRect(textbox.x() + 5, textbox.y() + 5,
                        textbox.width() - 10, textbox.height() - 10)
        painter = QPainter(self)
        pixmap = self.splash_gif.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)
        painter.drawPixmap(self.rect(), pixmap)
        painter.setPen(QColor(Qt.black))
       
    
    def sizeHint(self):
    
        return self.splash_gif.scaledSize()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    movie = QMovie("s2.gif")
    splash = IntroSplashScreen(movie)
    splash.show()
    
    start = time.time()
    
    while movie.state() == QMovie.Running and time.time() < start + 10:
        app.processEvents()
    
    window = QWidget()
    window.show()
    splash.finish(window)
    
    sys.exit(app.exec_())